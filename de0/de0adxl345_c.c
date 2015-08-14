#include <errno.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include "py/runtime.h"

#define CONVERT_INT(name, type)                                                                     \
    type name;                                                                                      \
    if (MP_OBJ_IS_INT(name ## _in)) {                                                               \
        name = mp_obj_get_int_truncated(name ## _in);                                               \
    } else {                                                                                        \
        nlr_raise(mp_obj_new_exception_msg(&mp_type_TypeError, #name " should be of type " #type)); \
        return mp_obj_new_int(-1);                                                                  \
    }

STATIC mp_obj_t mod_de0adxl345_c_reg_write(mp_obj_t file_in, mp_obj_t address_in, mp_obj_t value_in) {
    CONVERT_INT(file, int);
    CONVERT_INT(address, uint8_t);
    CONVERT_INT(value, uint8_t);

    uint8_t szValue[2];
    
    // write to define register
    szValue[0] = address;
    szValue[1] = value;
    if (write(file, &szValue, sizeof(szValue)) != sizeof(szValue)) {
        nlr_raise(mp_obj_new_exception_msg(&mp_type_RuntimeError, "reg_write didn't succeed"));
    }
    
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_3(mod_de0adxl345_c_reg_write_obj, mod_de0adxl345_c_reg_write);

STATIC mp_obj_t mod_de0adxl345_c_reg_read(mp_obj_t file_in, mp_obj_t address_in) {
    CONVERT_INT(file, int);
    CONVERT_INT(address, uint8_t);

    // write to define register
    if (write(file, &address, sizeof(address)) != sizeof(address)) {
        nlr_raise(mp_obj_new_exception_msg(&mp_type_RuntimeError, "reg_read didn't succeed in writing the address"));
    }

    // read back value
    uint8_t value;
    if (read(file, &value, sizeof(value)) != sizeof(value)) {
        nlr_raise(mp_obj_new_exception_msg(&mp_type_RuntimeError, "reg_read didn't succeed in reading the value"));
    }

    return mp_obj_new_int_from_uint(value);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(mod_de0adxl345_c_reg_read_obj, mod_de0adxl345_c_reg_read);

STATIC mp_obj_t mod_de0adxl345_c_reg_multi_read(mp_obj_t file_in, mp_obj_t address_in, mp_obj_t len_in) {
    CONVERT_INT(file, int);
    CONVERT_INT(address, uint8_t);
    CONVERT_INT(len, mp_uint_t);

    if (write(file, &address, sizeof(address)) != sizeof(address)) {
        nlr_raise(mp_obj_new_exception_msg(&mp_type_RuntimeError, "reg_multi_read didn't succeed in writing the address"));
    }

    uint8_t readdata[len];
    if (read(file, readdata, len) != len) {
        nlr_raise(mp_obj_new_exception_msg(&mp_type_RuntimeError, "reg_multi_read didn't succeed in reading the values"));
    }

    mp_obj_t readdata_out[len];
    for (size_t idx = 0; idx < len; ++idx) {
        readdata_out[idx] = mp_obj_new_int_from_uint(readdata[idx]);
    }

    return mp_obj_new_list(len, readdata_out);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_3(mod_de0adxl345_c_reg_multi_read_obj, mod_de0adxl345_c_reg_multi_read);

STATIC mp_obj_t mod_de0adxl345_c_init(void) {
    int file;
    const char *filename = "/dev/i2c-0";

    if ((file = open(filename, O_RDWR)) < 0) {
        nlr_raise(mp_obj_new_exception_msg(&mp_type_RuntimeError, "init didn't succeed in opening i2c"));
    }

    int addr = 0b01010011;
    if (ioctl(file, I2C_SLAVE, addr) < 0) {
        nlr_raise(mp_obj_new_exception_msg(&mp_type_RuntimeError, "init didn't succeed in aquire bus"));
    }

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(mod_de0adxl345_c_init_obj, mod_de0adxl345_c_init);

STATIC const mp_map_elem_t mp_module_de0adxl345_c_globals_table[] = {
    { MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_OBJ_NEW_QSTR(MP_QSTR_de0adxl345_c) },

#define FUN(name) { MP_OBJ_NEW_QSTR(MP_QSTR_ ## name), (mp_obj_t)&mod_de0adxl345_c_ ## name ## _obj }

    FUN(reg_read),
    FUN(reg_write),
    FUN(reg_multi_read),
    FUN(init),

#undef FUN

};

STATIC MP_DEFINE_CONST_DICT(mp_module_de0adxl345_c_globals, mp_module_de0adxl345_c_globals_table);

const mp_obj_module_t mp_module_de0adxl345_c = {
    .base = { &mp_type_module },
    .name = MP_QSTR_de0adxl345_c,
    .globals = (mp_obj_dict_t *)&mp_module_de0adxl345_c_globals,
};