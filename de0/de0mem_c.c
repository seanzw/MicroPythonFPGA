//**********************************************************
// Basic memory access.
//**********************************************************

#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <stdio.h>
#include "py/runtime.h"        // micropython api

// ===============================
// mmap(pa: int, nbytes: int): int
// ===============================
// map physical address [pa, pa + nbytes), return virtual address base
// 
STATIC mp_obj_t mod_de0mem_c_mmap(mp_obj_t pa_in, mp_obj_t nbytes_in) {
    mp_uint_t pa;
    mp_uint_t nbytes;
    int fd;
    mp_uint_t va;
    
    if (MP_OBJ_IS_INT(pa_in)) {
        pa = mp_obj_get_int_truncated(pa_in);
    } else {
        // printf("pa is not int");
        return mp_obj_new_int(-1);
    }
    
    if (MP_OBJ_IS_INT(nbytes_in)) {
        nbytes = mp_obj_get_int_truncated(nbytes_in);
    } else {
        // printf("nbytes is not int");
        return mp_obj_new_int(-2);
    }
    
    // Open the memory as a file
    if ((fd = open("/dev/mem", O_RDWR | O_SYNC)) < 0) {
        // printf("Cannot open file");
        return mp_obj_new_int(-3);
    }
    
    // Call mmap
    if ((va = (mp_uint_t)mmap(NULL, nbytes, PROT_READ | PROT_WRITE, MAP_SHARED, fd, pa)) == -1) {
        // printf("Cannot mmap");
        return mp_obj_new_int(-4);
    }
    
    if (close(fd) < 0) {
        // printf("Cannot close");
        return mp_obj_new_int(-5);
    }
    
    return mp_obj_new_int_from_uint(va);
}

STATIC MP_DEFINE_CONST_FUN_OBJ_2(mod_de0mem_c_mmap_obj, mod_de0mem_c_mmap);


// Write various types of integers to virtual address
#define CREATE_WRITE_FUNC(T)                                                                 \
    STATIC mp_obj_t mod_de0mem_c_write_ ## T ## _to_va(mp_obj_t va_in, mp_obj_t val_in) {    \
        mp_uint_t va;                                                                        \
        mp_int_t val;                                                                        \
                                                                                             \
        if (MP_OBJ_IS_INT(va_in)) {                                                          \
            va = mp_obj_get_int_truncated(va_in);                                            \
        } else {                                                                             \
            return mp_obj_new_int(-1);                                                       \
        }                                                                                    \
                                                                                             \
        if (MP_OBJ_IS_INT(val_in)) {                                                         \
            val = mp_obj_get_int_truncated(val_in);                                          \
        } else {                                                                             \
            return mp_obj_new_int(-1);                                                       \
        }                                                                                    \
                                                                                             \
        *(T ## _t *)va = (T ## _t)val;                                                       \
                                                                                             \
        return mp_obj_new_int(0);                                                            \
    }                                                                                        \
                                                                                             \
    STATIC MP_DEFINE_CONST_FUN_OBJ_2(mod_de0mem_c_write_ ## T ## _to_va_obj, mod_de0mem_c_write_ ## T ## _to_va);

CREATE_WRITE_FUNC(int8)
CREATE_WRITE_FUNC(uint8)
CREATE_WRITE_FUNC(int16)
CREATE_WRITE_FUNC(uint16)
CREATE_WRITE_FUNC(int32)
CREATE_WRITE_FUNC(uint32)

// Read various types of integers from virtual address

#define CREATE_READ_SIGNED_FUNC(T) \
    STATIC mp_obj_t mod_de0mem_c_read_ ## T ## _from_va(mp_obj_t va_in) {                    \
        mp_uint_t va;                                                                        \
        mp_int_t val;                                                                        \
                                                                                             \
        if (MP_OBJ_IS_INT(va_in)) {                                                          \
            va = mp_obj_get_int_truncated(va_in);                                            \
        } else {                                                                             \
            return mp_obj_new_int(-1);                                                       \
        }                                                                                    \
                                                                                             \
        val = *(T ## _t *)va;                                                                \
                                                                                             \
        return mp_obj_new_int(val);                                                          \
    }                                                                                        \
                                                                                             \
    STATIC MP_DEFINE_CONST_FUN_OBJ_1(mod_de0mem_c_read_ ## T ## _from_va_obj, mod_de0mem_c_read_ ## T ## _from_va);

CREATE_READ_SIGNED_FUNC(int8)
CREATE_READ_SIGNED_FUNC(int16)
CREATE_READ_SIGNED_FUNC(int32)

// Read various types of integers from virtual address
#define CREATE_READ_UNSIGNED_FUNC(T) \
    STATIC mp_obj_t mod_de0mem_c_read_ ## T ## _from_va(mp_obj_t va_in) {                    \
        mp_uint_t va;                                                                        \
        mp_uint_t val;                                                                       \
                                                                                             \
        if (MP_OBJ_IS_INT(va_in)) {                                                          \
            va = mp_obj_get_int_truncated(va_in);                                            \
        } else {                                                                             \
            return mp_obj_new_int(-1);                                                       \
        }                                                                                    \
                                                                                             \
        val = *(T ## _t *)va;                                                                \
                                                                                             \
        return mp_obj_new_int_from_uint(val);                                                \
    }                                                                                        \
                                                                                             \
    STATIC MP_DEFINE_CONST_FUN_OBJ_1(mod_de0mem_c_read_ ## T ## _from_va_obj, mod_de0mem_c_read_ ## T ## _from_va);

CREATE_READ_UNSIGNED_FUNC(uint8)
CREATE_READ_UNSIGNED_FUNC(uint16)
CREATE_READ_UNSIGNED_FUNC(uint32)

STATIC const mp_map_elem_t mp_module_de0mem_c_globals_table[] = {
    { MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_OBJ_NEW_QSTR(MP_QSTR_de0mem_c) },

#define FUN(name) { MP_OBJ_NEW_QSTR(MP_QSTR_ ## name), (mp_obj_t)&mod_de0mem_c_ ## name ## _obj }

    FUN(mmap),
    FUN(write_int8_to_va),
    FUN(write_uint8_to_va),
    FUN(write_int16_to_va),
    FUN(write_uint16_to_va),
    FUN(write_int32_to_va),
    FUN(write_uint32_to_va),
    FUN(read_int8_from_va),
    FUN(read_int16_from_va),
    FUN(read_int32_from_va),
    FUN(read_uint8_from_va),
    FUN(read_uint16_from_va),
    FUN(read_uint32_from_va),
#undef FUN

};

STATIC MP_DEFINE_CONST_DICT(mp_module_de0mem_c_globals, mp_module_de0mem_c_globals_table);

const mp_obj_module_t mp_module_de0mem_c = {
    .base = { &mp_type_module },
    .name = MP_QSTR_de0mem_c,
    .globals = (mp_obj_dict_t *)&mp_module_de0mem_c_globals,
};