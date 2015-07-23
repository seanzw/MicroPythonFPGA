###############################################################################
# unix-cpy/Makefile
###############################################################################

include ../py/mkenv.mk

PROG = cpy
	# what is PROG?

include ../py/py.mk

INC = -I.
	# add current dir as include dir
INC += -I..
	# add .. as include dir
INC += -I$(BUILD)
	# BUILD is defined in ../py/mkenv.mk

CFLAGS = $(INC) -Wall -Wpointer-arith -Werror -ansi -std=gnu99 -DUNIX
	# add a '#define UNIX'.
	# I greped 'UNIX' and it seemed that it is not used.
	# I commented it out and it seemed okay.

LDFLAGS = -lm
	# link math library

ifdef DEBUG
	# where is DEBUG defined?
CFLAGS += -O0 -g
else
CFLAGS += -Os

SRC_C = \
	main.c \
	# set source file

OBJ = $(PY_O) $(addprefix $(BUILD)/, $(SRC_C:.c=.o))
	# Makefile has functions which are called by $(func arg1, arg2, ...)
	# where is PY_O defined?
LIB = 

include ../py/mkrules.mk 


###############################################################################
# py/mkenv.mk
###############################################################################

ifneq ($(lastword a b), b)
$(error These Makefiles require make 3.81 or newer)
endif
	# This looks unimportant
	
THIS_MAKEFILE := $(lastword $(MAKEFILE_LIST))
	# MAKEFILE_LIST == ../py/mkenv.mk
	# $(lastword $(MAKEFILE_LIST)) == ../py/mkenv.mk
	# THIS_MAKEFILE == ../py/mkenv.mk
	
TOP := $(patsubst %/py/mkenv.mk, %, $(THIS_MAKEFILE))
	# TOP == ..
	
ifeq ("$(origin V)", "command line")
BUILD_VERBOSE=$(V)
endif
	# if the user added a V option in command line (-V=1)

ifndef BUILD_VERBOSE
BUILD_VERBOSE = 0
endif
	# set BUILD_VERBOSE

ifeq ($(BUILD_VERBOSE), 0)
Q = @
else
Q = 
endif
	# @ disable command line output.

# Since this is a new feature, advertise it
ifeq ($(BUILD_VERBOSE),0)
$(info Use make V=1 or set BUILD_VERBOSE in your environment to increase build verbosity.)
endif

PY_SRC ?= $(TOP)/py
	# ?= only set when the variable doesn't have a value yet
BUILD ?= build

RM = rm
ECHO = @echo
CP = cp
MKDIR = mkdir
SED = sed
PYTHON = python

AS = $(CROSS_COMPILE)as
CC = $(CROSS_COMPILE)gcc
LD = $(CROSS_COMPILE)ld
OBJCOPY = $(CROSS_COMPILE)objcopy
SIZE = $(CROSS_COMPILE)size
STRIP = $(CROSS_COMPILE)strip

all:
	# a rule called all
.PHONY: all

.DELETE_ON_ERROR:

MKENV_INCLUDED = 1

###############################################################################
# py/py.mk
###############################################################################

PY_BUILD = $(BUILD)/py
	# every C file ../py/*.c will be compiled to build/py/*.o

HEADER_BUILD = $(BUILD)/genhdr
	# some auto-generated header files will be put in build/genhdr

PY_QSTR_DEFS = $(PY_SRC)/qstrdefs.h
	# ../py/qstrdefs.h

CSUPEROPT = -O3
	# level 3 optimization

PY_O_BASENAME = \
	mpstate.o \
	nlrx86.o \
	nlrx64.o \
	nlrthumb.o \
	nlrxtensa.o \
	nlrsetjmp.o \
	malloc.o \
	gc.o \
	qstr.o \
	vstr.o \
	mpprint.o \
	unicode.o \
	mpz.o \
	lexer.o \
	lexerstr.o \
	lexerunix.o \
	parse.o \
	scope.o \
	compile.o \
	emitcommon.o \
	emitcpy.o \
	emitbc.o \
	asmx64.o \
	emitnx64.o \
	asmx86.o \
	emitnx86.o \
	asmthumb.o \
	emitnthumb.o \
	emitinlinethumb.o \
	asmarm.o \
	emitnarm.o \
	formatfloat.o \
	parsenumbase.o \
	parsenum.o \
	emitglue.o \
	runtime.o \
	nativeglue.o \
	stackctrl.o \
	argcheck.o \
	warning.o \
	map.o \
	obj.o \
	objarray.o \
	objattrtuple.o \
	objbool.o \
	objboundmeth.o \
	objcell.o \
	objclosure.o \
	objcomplex.o \
	objdict.o \
	objenumerate.o \
	objexcept.o \
	objfilter.o \
	objfloat.o \
	objfun.o \
	objgenerator.o \
	objgetitemiter.o \
	objint.o \
	objint_longlong.o \
	objint_mpz.o \
	objlist.o \
	objmap.o \
	objmodule.o \
	objobject.o \
	objproperty.o \
	objnone.o \
	objnamedtuple.o \
	objrange.o \
	objreversed.o \
	objset.o \
	objsingleton.o \
	objslice.o \
	objstr.o \
	objstrunicode.o \
	objstringio.o \
	objtuple.o \
	objtype.o \
	objzip.o \
	opmethods.o \
	sequence.o \
	stream.o \
	binary.o \
	builtinimport.o \
	builtinevex.o \
	modarray.o \
	modbuiltins.o \
	modcollections.o \
	modgc.o \
	modio.o \
	modmath.o \
	modcmath.o \
	modmicropython.o \
	modstruct.o \
	modsys.o \
	vm.o \
	bc.o \
	showbc.o \
	repl.o \
	smallint.o \
	frozenmod.o \
	../extmod/moductypes.o \
	../extmod/modujson.o \
	../extmod/modure.o \
	../extmod/moduzlib.o \
	../extmod/moduheapq.o \
	../extmod/moduhashlib.o \
	../extmod/modubinascii.o \
	../extmod/modmachine.o \

	# These are the .o files
	# What .c files are they from?

PY_O = $(addprefix $(PY_BUILD)/, $(PY_O_BASENAME))
	# prepend every .o file name with build/

FORCE:
.PHONY: FORCE

$(HEADER_BUILD)/mpversion.h: FORCE | $(HEADER_BUILD)
	# $(HEADER_BUILD) is an "order-only prerequisite":
	# 1. If somebody explicitly calls $(HEADER_BUILD)/mpversion.h to be built, then
	#     $(HEADER_BUILD) will be automatically called.
	# 2. If $(HEADER_BUILD) becomes newer, then
	#     $(HEADER_BUILD)/mpversion.h will not be automatically called.

	$(Q)$(PYTHON) $(PY_SRC)/makeversionhdr.py $@
		# This is the actual command for $(HEADER_BUILD)/mpversion.h:
		# ../py/makeversionhdr.py <arguments>
		# Where do the arguments come from?

MPCONFIGPORT_MK = $(wildcard mpconfigport.mk)
	# MPCONFIGPORT_MK == mpconfigport.mk if mpconfigport.mk exists

$(HEADER_BUILD)/qstrdefs.generated.h: $(PY_QSTR_DEFS) $(QSTR_DEFS) $(PY_SRC)/makeqstrdata.py mpconfigport.h $(MPCONFIGPORT_MK) $(PY_SRC)/mpconfig.h | $(HEADER_BUILD)
	# Depends on:
	#     $(PY_QSTR_DEFS)           == ../py/qstrdefs.h (defined in ../py/py.mk)
	#     $(QSTR_DEFS)              == qstrdefsport.h (defined in Makefile)
	#     $(PY_SRC)/makeqstrdata.py == ../py/makeqstrdata.py
	#     $(MPCONFIGPORT_MK)        == mpconfigport.mk (if exists)
	#     $(PY_SRC)/mpconfig.h      == ../py/mpconfig.h
	$(ECHO) "GEN $@"
		# Just print a line.
	$(Q)cat $(PY_QSTR_DEFS) $(QSTR_DEFS) | $(SED) 's/^Q(.*)/"&"/' | $(CPP) $(CFLAGS) - | sed 's/^"\(Q(.*)\)"/\1/' > $(HEADER_BUILD)/qstrdefs.preprocessed.h
		# cat ../py/qstrdefs.h qstrdefsport.h | sed 's/^Q(.*)/"&"/' | $(CPP) $(CFLAGS) - | sed 's/^"\(Q(.*)\)"/\1/' > $(HEADER_BUILD)/qstrdefs.preprocessed.h
		# 1. Concat files "../py/qstrdefs.h" and "qstrdefsport.h" into a single file
		# 2. Replace any Q(...) with "Q(...)"
		# 3. Use g++
		# 4. Replace any "Q(...)" with Q(...)
		# 5. Save as build/genhdr/qstrdefs.preprocessed.h
	$(Q)$(PYTHON) $(PY_SRC)/makeqstrdata.py $(HEADER_BUILD)/qstrdefs.preprocessed.h > $@
		# python ../py/makeqstrdata.py build/genhdr/qstrdefs.preprocessed.h > $@
		# What is $@?

# The following files are not originally in ../py.

$(PY_BUILD)/emitnx64.o: CFLAGS += -DN_X64
	# Add #define N_X64
$(PY_BUILD)/emitnx64.o: py/emitnative.c
	$(call compile_c)

$(PY_BUILD)/emitnx86.o: CFLAGS += -DN_X86
$(PY_BUILD)/emitnx86.o: py/emitnative.c
	$(call compile_c)

$(PY_BUILD)/emitnthumb.o: CFLAGS += -DN_THUMB
$(PY_BUILD)/emitnthumb.o: py/emitnative.c
	$(call compile_c)

$(PY_BUILD)/emitnarm.o: CFLAGS += -DN_ARM
$(PY_BUILD)/emitnarm.o: py/emitnative.c
	$(call compile_c)

$(PY_BUILD)/gc.o: CFLAGS += $(CSUPEROPT)
	# CFLAGS += -O3

$(PY_BUILD)/vm.o: CFLAGS += $(CSUPEROPT)
	# CFLAGS += -O3

###############################################################################
# py/mkrules.mk
###############################################################################

ifneq ($(MKENV_INCLUDED), 1)
THIS_MAKEFILE = $(lastword $(MAKEFILE_LIST))
include $(dir $(THIS_MAKEFILE))mkenv.mk
endif
	# If ../py/mkenv.mk is not included yet, include it.

vpath %.S . $(TOP)
	# For any *.S in . and ..
$(BUILD)/%.o: %.S
	$(ECHO) "CC $<"
	$(Q)$(CC) $(CFLAGS) -c -o $@ $<
		# Tell gcc to compile and assemble, and generate .o file.
		# $@ is the name of the file being generated.
		# $< the first prerequisite.

vpath %.s . $(TOP)
	# For any *.s in . and ..
$(BUILD)/%.o: %.s
	$(ECHO) "AS $<"
	$(Q)$(AS) -o $@ $<
		# Tell as to assemble, and generate .o file.

define compile_c
$(ECHO) "CC $<"
$(Q)$(CC) $(CFLAGS) -c -MD -o $@ $<
@$(CP) $(@:.o=.d) $(@:.o=.P); \
  $(SED) -e 's/#.*//' e 's/^.*': *//' -c 's/ *\\$$//' \
    -e '/^$$/ d' -e 's/$$/ :/' < $(@:.o=.d) >> $(@:.o=.P); \
  $(RM) -f $(@:.o=.d)
endef

vpath %.c . $(TOP)
	# For any .c in . and ..
$(BUILD)/%.o: %.c
	$(call compile_c)

$(BUILD)/%.pp: %.c
	$(ECHO) "Preprocess $<"
	$(Q)$(CC) $(CFLAGS) -E -Wp,-C,-dD,-dI -o $@ $<
	