/*
 * This file is part of the Micro Python project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2013, 2014 Damien P. George
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

// options to control how Micro Python is built

#define MICROPY_ALLOC_PATH_MAX      (PATH_MAX)
#if !defined(MICROPY_EMIT_X64) && defined(__x86_64__)
    #define MICROPY_EMIT_X64        (1)
#endif
#if !defined(MICROPY_EMIT_X86) && defined(__i386__)
    #define MICROPY_EMIT_X86        (1)
#endif
#if !defined(MICROPY_EMIT_THUMB) && defined(__thumb2__)
    #define MICROPY_EMIT_THUMB      (1)
    #define MICROPY_MAKE_POINTER_CALLABLE(p) ((void*)((mp_uint_t)(p) | 1))
#endif
// Some compilers define __thumb2__ and __arm__ at the same time, let
// autodetected thumb2 emitter have priority.
#if !defined(MICROPY_EMIT_ARM) && defined(__arm__) && !defined(__thumb2__)
    #define MICROPY_EMIT_ARM        (1)
#endif
#define MICROPY_COMP_MODULE_CONST   (1)
#define MICROPY_COMP_TRIPLE_TUPLE_ASSIGN (1)
#define MICROPY_ENABLE_GC           (1)
#define MICROPY_ENABLE_FINALISER    (1)
#define MICROPY_STACK_CHECK         (1)
#define MICROPY_MALLOC_USES_ALLOCATED_SIZE (1)
#define MICROPY_MEM_STATS           (1)
#define MICROPY_DEBUG_PRINTERS      (1)
#define MICROPY_USE_READLINE_HISTORY (1)
#define MICROPY_HELPER_REPL         (1)
#define MICROPY_HELPER_LEXER_UNIX   (1)
#define MICROPY_ENABLE_SOURCE_LINE  (1)
#define MICROPY_FLOAT_IMPL          (MICROPY_FLOAT_IMPL_DOUBLE)
#define MICROPY_LONGINT_IMPL        (MICROPY_LONGINT_IMPL_MPZ)
#define MICROPY_STREAMS_NON_BLOCK   (1)
#define MICROPY_OPT_COMPUTED_GOTO   (1)
#define MICROPY_OPT_CACHE_MAP_LOOKUP_IN_BYTECODE (1)
#define MICROPY_CAN_OVERRIDE_BUILTINS (1)
#define MICROPY_PY_FUNCTION_ATTRS   (1)
#define MICROPY_PY_DESCRIPTORS      (1)
#define MICROPY_PY_BUILTINS_STR_UNICODE (1)
#define MICROPY_PY_BUILTINS_STR_SPLITLINES (1)
#define MICROPY_PY_BUILTINS_MEMORYVIEW (1)
#define MICROPY_PY_BUILTINS_FROZENSET (1)
#define MICROPY_PY_BUILTINS_COMPILE (1)
#define MICROPY_PY_BUILTINS_NOTIMPLEMENTED (1)
#define MICROPY_PY_MICROPYTHON_MEM_INFO (1)
#define MICROPY_PY_ALL_SPECIAL_METHODS (1)
#define MICROPY_PY_ARRAY_SLICE_ASSIGN (1)
#define MICROPY_PY_SYS_EXIT         (1)
#define MICROPY_PY_SYS_PLATFORM     "linux"
#define MICROPY_PY_SYS_MAXSIZE      (1)
#define MICROPY_PY_SYS_STDFILES     (1)
#define MICROPY_PY_SYS_EXC_INFO     (1)
#define MICROPY_PY_COLLECTIONS_ORDEREDDICT (1)
#define MICROPY_PY_MATH_SPECIAL_FUNCTIONS (1)
#define MICROPY_PY_CMATH            (1)
#define MICROPY_PY_IO_FILEIO        (1)
#define MICROPY_PY_GC_COLLECT_RETVAL (1)
#define MICROPY_MODULE_FROZEN       (1)

#define MICROPY_STACKLESS           (0)
#define MICROPY_STACKLESS_STRICT    (0)

#define MICROPY_PY_UCTYPES          (1)
#define MICROPY_PY_UZLIB            (1)
#define MICROPY_PY_UJSON            (1)
#define MICROPY_PY_URE              (1)
#define MICROPY_PY_UHEAPQ           (1)
#define MICROPY_PY_UHASHLIB         (1)
#define MICROPY_PY_UBINASCII        (1)
#define MICROPY_PY_MACHINE          (1)

// Define to MICROPY_ERROR_REPORTING_DETAILED to get function, etc.
// names in exception messages (may require more RAM).
#define MICROPY_ERROR_REPORTING     (MICROPY_ERROR_REPORTING_DETAILED)
#define MICROPY_WARNINGS            (1)

// Define to 1 to use undertested inefficient GC helper implementation
// (if more efficient arch-specific one is not available).
#ifndef MICROPY_GCREGS_SETJMP
    #ifdef __mips__
        #define MICROPY_GCREGS_SETJMP (1)
    #else
        #define MICROPY_GCREGS_SETJMP (0)
    #endif
#endif

#define MICROPY_ENABLE_EMERGENCY_EXCEPTION_BUF   (1)
#define MICROPY_EMERGENCY_EXCEPTION_BUF_SIZE  (256)

extern const struct _mp_obj_module_t mp_module_os;
extern const struct _mp_obj_module_t mp_module_time;
extern const struct _mp_obj_module_t mp_module_termios;
extern const struct _mp_obj_module_t mp_module_socket;
extern const struct _mp_obj_module_t mp_module_ffi;
extern const struct _mp_obj_module_t mp_module_de0mem_c;
extern const struct _mp_obj_module_t mp_module_de0adxl345_c;

#if MICROPY_PY_FFI
#define MICROPY_PY_FFI_DEF { MP_OBJ_NEW_QSTR(MP_QSTR_ffi), (mp_obj_t)&mp_module_ffi },
#else
#define MICROPY_PY_FFI_DEF
#endif
#if MICROPY_PY_TIME
#define MICROPY_PY_TIME_DEF { MP_OBJ_NEW_QSTR(MP_QSTR_utime), (mp_obj_t)&mp_module_time },
#else
#define MICROPY_PY_TIME_DEF
#endif
#if MICROPY_PY_TERMIOS
#define MICROPY_PY_TERMIOS_DEF { MP_OBJ_NEW_QSTR(MP_QSTR_termios), (mp_obj_t)&mp_module_termios },
#else
#define MICROPY_PY_TERMIOS_DEF
#endif
#if MICROPY_PY_SOCKET
#define MICROPY_PY_SOCKET_DEF { MP_OBJ_NEW_QSTR(MP_QSTR_usocket), (mp_obj_t)&mp_module_socket },
#else
#define MICROPY_PY_SOCKET_DEF
#endif
#if MICROPY_PY_DE0
#define MICROPY_PY_DE0MEM_DEF { MP_OBJ_NEW_QSTR(MP_QSTR_de0mem_c), (mp_obj_t)&mp_module_de0mem_c },
#define MICROPY_PY_DE0ADXL345_DEF { MP_OBJ_NEW_QSTR(MP_QSTR_de0adxl345_c), (mp_obj_t)&mp_module_de0adxl345_c },
#else
#define MICROPY_PY_DE0MEM_DEF
#endif

#define MICROPY_PORT_BUILTIN_MODULES \
    MICROPY_PY_DE0MEM_DEF \
    MICROPY_PY_DE0ADXL345_DEF \
    MICROPY_PY_FFI_DEF \
    MICROPY_PY_TIME_DEF \
    MICROPY_PY_SOCKET_DEF \
    { MP_OBJ_NEW_QSTR(MP_QSTR__os), (mp_obj_t)&mp_module_os }, \
    MICROPY_PY_TERMIOS_DEF \

// type definitions for the specific machine

#ifdef __LP64__
typedef long mp_int_t; // must be pointer size
typedef unsigned long mp_uint_t; // must be pointer size
#else
// These are definitions for machines where sizeof(int) == sizeof(void*),
// regardless for actual size.
typedef int mp_int_t; // must be pointer size
typedef unsigned int mp_uint_t; // must be pointer size
#endif

#define BYTES_PER_WORD sizeof(mp_int_t)

// Cannot include <sys/types.h>, as it may lead to symbol name clashes
#if _FILE_OFFSET_BITS == 64 && !defined(__LP64__)
typedef long long mp_off_t;
#else
typedef long mp_off_t;
#endif

typedef void *machine_ptr_t; // must be of pointer size
typedef const void *machine_const_ptr_t; // must be of pointer size

void mp_unix_alloc_exec(mp_uint_t min_size, void** ptr, mp_uint_t *size);
void mp_unix_free_exec(void *ptr, mp_uint_t size);
void mp_unix_mark_exec(void);
#define MP_PLAT_ALLOC_EXEC(min_size, ptr, size) mp_unix_alloc_exec(min_size, ptr, size)
#define MP_PLAT_FREE_EXEC(ptr, size) mp_unix_free_exec(ptr, size)

#define MP_PLAT_PRINT_STRN(str, len) fwrite(str, 1, len, stdout)

#ifdef __linux__
// Can access physical memory using /dev/mem
#define MICROPY_PLAT_DEV_MEM  (1)
#endif

extern const struct _mp_obj_fun_builtin_t mp_builtin_input_obj;
extern const struct _mp_obj_fun_builtin_t mp_builtin_open_obj;
#define MICROPY_PORT_BUILTINS \
    { MP_OBJ_NEW_QSTR(MP_QSTR_input), (mp_obj_t)&mp_builtin_input_obj }, \
    { MP_OBJ_NEW_QSTR(MP_QSTR_open), (mp_obj_t)&mp_builtin_open_obj },

#define MP_STATE_PORT MP_STATE_VM

#define MICROPY_PORT_ROOT_POINTERS \
    const char *readline_hist[50]; \
    mp_obj_t keyboard_interrupt_obj; \
    void *mmap_region_head; \

#define MICROPY_HAL_H "unix_mphal.h"

// We need to provide a declaration/definition of alloca()
#ifdef __FreeBSD__
#include <stdlib.h>
#else
#include <alloca.h>
#endif
