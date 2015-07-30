//********************************************************************
// Try to create a micropython module for de0 FPGA.
//********************************************************************
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <time.h>
#include <sys/mman.h>
#include "hwlib.h"
#include "socal/socal.h"
#include "socal/hps.h"
#include "socal/alt_gpio.h"
#include "hps_0.h"
#include "led.h"
#include <stdbool.h>

#include <string.h>
#include "py/runtime.h"

#define HW_REGS_BASE ( ALT_STM_OFST )
#define HW_REGS_SPAN ( 0x04000000 )
#define HW_REGS_MASK ( HW_REGS_SPAN - 1 )

volatile unsigned long *h2p_lw_led_addr=NULL;

STATIC mp_obj_t mod_de0_helloworld(void) {
    const char *sentence = "Hello from DE0-NANO-SOC!\n";
    return mp_obj_new_str(sentence, (mp_uint_t)strlen(sentence), false);
}

STATIC mp_obj_t mod_de0_led_fancy(void) {

    void *virtual_base;
    int fd;
    int i;

    // map the address space for the LED registers into user space so we can interact with them.
    // we'll actually map in the entire CSR span of the HPS since we want to access various registers within that span
    if( ( fd = open( "/dev/mem", ( O_RDWR | O_SYNC ) ) ) == -1 ) {
        const char *errormem = "ERROR: could not open \"/dev/mem\"...";
        return mp_obj_new_str(errormem, (mp_uint_t)strlen(errormem), false);
    }
    virtual_base = mmap( NULL, HW_REGS_SPAN, ( PROT_READ | PROT_WRITE ), MAP_SHARED, fd, HW_REGS_BASE );    
    if( virtual_base == MAP_FAILED ) {
        const char *errormmapfailed = "ERROR: mmap() failed...";
        close( fd );
        return mp_obj_new_str(errormmapfailed, (mp_uint_t)strlen(errormmapfailed), false);
    }
    h2p_lw_led_addr = (unsigned long *)((unsigned long)virtual_base + ((unsigned long)(ALT_LWFPGASLVS_OFST + LED_PIO_BASE) & (unsigned long)(HW_REGS_MASK)));

    int times = 0;
    while(times <= 100)
    {
        printf("LED ON \r\n");
        for(i=0;i<=8;i++){
            LEDR_LightCount(i);
            usleep(100*1000);
        }
        printf("LED OFF \r\n");
        for(i=0;i<=8;i++){
            LEDR_OffCount(i);
            usleep(100*1000);
        }

        times++;
    }
    if( munmap( virtual_base, HW_REGS_SPAN ) != 0 ) {
        const char *errormunmap = "ERROR: munmap() failed...";
        close( fd );
        return mp_obj_new_str(errormunmap, (mp_uint_t)strlen(errormunmap), false);

    }
    close( fd );
    const char *shouldreturn = "i am done with the leds!";
    return mp_obj_new_str(shouldreturn, (mp_uint_t)strlen(shouldreturn), false);
}

STATIC MP_DEFINE_CONST_FUN_OBJ_0(mod_de0_helloworld_obj, mod_de0_helloworld);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(mod_de0_led_fancy_obj, mod_de0_led_fancy);

STATIC const mp_map_elem_t mp_module_de0_globals_table[] = {
    { MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_OBJ_NEW_QSTR(MP_QSTR_de0) },
    { MP_OBJ_NEW_QSTR(MP_QSTR_helloworld), (mp_obj_t)&mod_de0_helloworld_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_led_fancy), (mp_obj_t)&mod_de0_led_fancy_obj },
};

STATIC MP_DEFINE_CONST_DICT(mp_module_de0_globals, mp_module_de0_globals_table);

const mp_obj_module_t mp_module_de0 = {
    .base = { &mp_type_module },
    .name = MP_QSTR_de0,
    .globals = (mp_obj_dict_t*)&mp_module_de0_globals,
};
