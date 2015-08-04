#! /usr/bin/env python

# This script can translate auto-generated .h files into .py files.
# Derived from http://svn.python.org/projects/python/trunk/Tools/scripts/h2py.py

import sys, re, getopt, os

p_name = re.compile('^([a-zA-Z_][a-zA-Z0-9_]*)[\t ]*')

p_define = re.compile('^[\t ]*#[\t ]*define[\t ]+([a-zA-Z0-9_]+)[\t ]+')
# space = < '\t' | ' ' >
# ch = < 'a'-'z' | 'A'-'Z' | '0'-'9' | '_' >
# p_define = {space}* '#' {space}* 'define' {space}+ {ch}+ {space}+ 

p_comment = re.compile(r'/\*([^*]+|\*+[^/])*(\*+/)?')
# p_comment = '/*' ...

p_cpp_comment = re.compile('//.*')

ignores = [p_comment, p_cpp_comment]

p_char = re.compile(r"'(\\.[^\\]*|[^\\])'")

p_hex = re.compile(r"0x([0-9a-fA-F]+)L?")

def main():
    opts, args = getopt.getopt(sys.argv[1:], 'i:')
    for o, a in opts:
        if o == '-i':
            ignores.append(re.compile(a))
    if not args:
        args = ['-']
    for filename in args:
        if filename == '-':
            sys.stdout.write('Usage: python h2py.py file1, file2, ...\n')
            return None
            
        else:
            fp = open(filename, 'r')
            outfile = os.path.basename(filename)
            
            i = outfile.rfind('.')
            if i > 0:
                outfile = outfile[:i]
                
            modname = outfile.lower()
            outfile = modname + '.py'

            vals = process(fp)
            fp.close()
            
            outfp = open(modname.lower() + '.py', 'w')
            COMP_NAMES = [name[:-len('_COMPONENT_NAME')] for (name, body) in vals if name.endswith('_COMPONENT_NAME')]
            for comp_name in COMP_NAMES:
                outfp.write('class %s:\n' % comp_name.upper())
                for (attrib, body) in [(name[len(comp_name) + 1 : ], body) for (name, body) in vals if name.startswith(comp_name)]:
                    outfp.write('    %s = %s\n' % (attrib.upper(), body))
                outfp.write('\n')
            outfp.close()

def pytify(body):
    # replace ignored patterns by spaces
    for p in ignores:
        body = p.sub(' ', body)
        
    # replace char literals by ord(...)
    body = p_char.sub('ord(\\0)', body)
    
    # Compute negative hexadecimal constants
    start = 0
    UMAX = 2 * (sys.maxint + 1)
    while 1:
        m = p_hex.search(body, start)
        if not m: break
        s,e = m.span()
        val = long(body[slice(*m.span(1))], 16)
        if val > sys.maxint:
            val -= UMAX
            body = body[:s] + "(" + str(val) + ")" + body[e:]
        start = s + 1
    return body

def process(fp, env = {}):
    
    vals = []
    
    lineno = 0
    while 1:
        line = fp.readline()
        if not line:
            break
        lineno += 1
        
        match = p_define.match(line) # starts with '#define NAME '
        if match:
            # gobble up continuation lines
            while line[-2:] == '\\\n': # if ends with \ : need to add next line
                nextline = fp.readline()
                if not nextline:
                    break
                lineno += 1
                line += nextline
                
            name = match.group(1)
            body = line[match.end():].strip()
            body = pytify(body)
            
            if p_name.match(body):
                body = '"' + body + '"'
                
            ok = 0
            stmt = '%s = %s\n' % (name, body)
            try:
                exec stmt in env
            except:
                sys.stderr.write('Skipping: %s' % stmt)
            else:
                vals.append((name, body))

    return vals
    
if __name__ == '__main__':
    main()
