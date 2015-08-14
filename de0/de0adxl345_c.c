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

STATIC mp_obj_t mod_de0adxl345_c_reg_write(mp_obj_t file_in, mp_obj_t address_in, mp_obj_t value_in) {


    bool bSuccess = false;
    uint8_t szValue[2];
    
    // write to define register
    szValue[0] = address;
    szValue[1] = value;
    if (write(file, &szValue, sizeof(szValue)) == sizeof(szValue)){
            bSuccess = true;
    }
    
    return bSuccess;        
}

bool ADXL345_REG_READ(int file, uint8_t address,uint8_t *value){
    bool bSuccess = false;
    uint8_t Value;
    
    // write to define register
    if (write(file, &address, sizeof(address)) == sizeof(address)){
    
        // read back value
        if (read(file, &Value, sizeof(Value)) == sizeof(Value)){
            *value = Value;
            bSuccess = true;
        }
    }
        
    
    return bSuccess;    
}

bool ADXL345_REG_MULTI_READ(int file, uint8_t readaddr,uint8_t readdata[], uint8_t len){
    bool bSuccess = false;

    // write to define register
    if (write(file, &readaddr, sizeof(readaddr)) == sizeof(readaddr)){
        // read back value
        if (read(file, readdata, len) == len){
            bSuccess = true;
        }
    }
    
        
    return bSuccess;
}