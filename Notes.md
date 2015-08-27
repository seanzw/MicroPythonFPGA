
### RocketBoards Tutorials
http://rocketboards.org/foswiki/view/Documentation/WS1IntroToAlteraSoCDevices

### Software Installation
* Quartus II
* SoC EDS
* Serial terminal: Putty / screen

### SD Card Image
It creates 3 partitions: a FAT, a EXT3, and a 0xA2 partition.

### Preloader
The hardware BootROM finds and runs the preloader on the 0xA2 partition.

You can generate a preloader with bsp-editor, which needs a `hps_isw_handoff` folder.

### Tips
You can boot the target board into Linux and transfer file into the FAT partition without a SD card reader. Just mount it.
```
mount /dev/mmcblk0p1 /mnt
```
Notice that some time you will get an error as it is not properly unmounted. Try this:
```
echo -n "/dev/mmcblk0p1" > /sys/devices/sopc.0/ffb40000.usb/gadget/lun0/file
cat /sys/devices/sopc.0/ffb40000.usb/gadget/lun0/file
```

### Compilation methods tried
* `my_first_hps` on Windows embedded shell OK

* `my_first_hps` on Ubuntu64 without embedded shell OK

* `micropython/Windows` on VS OK

* `micropython/unix` on Ubuntu32, Ubuntu64 OK

* `micropython/unix` on OSX OK

        $ brew install pkg-config libffi
        $ export PKG_CONFIG_PATH=/usr/local/Cellar/libffi/3.0.13/lib/pkgconfig/

* `micropython/unix` on Windows Cygwin OK
    
        $ apt-cyg install libffi6 libffi-devel pkg-config
        $ export PKG_CONFIG_PATH="/lib/pkgconfig"

* `micropython/minimal` **without** CROSS_COMPILE on Mac Ubuntu64 OK

        $ make run

* `micropython/unix-cpy` CROSS_COMPILE on Windows embedded shell, Mac Ubuntu64 OK

### GC

In `py/gc.h`, there is the `gc_collect(): void`, but it needs to be implemented by the port, e.g. in `unix/gccollect.c`, or `minimal/main.c`.

In `bare-arm/main.c`:

    gc_collect(): void {} // empty function?

In `minimal/main.c`:

    gc_collect(): void { // WARNING: doesn't track CPU regs for root ptrs
        val dummy: void* // used to track stack boundary
        gc_collect_start()
        gc_collect_root(&dummy, (stack_top - &dummy) / int_size)
        gc_collect_end()
        gc_dump_info()
    }
    
In `unix/gccollect.c` (also used in Windows port):

    gc_collect(): void {
        gc_collect_start()
        val regs = gc_helper_get_regs() // this step requires hardware support!
        val regs_ptr: (void**)&regs // a pointer
        gc_collect_root(regs_ptr, (stack_top - &regs) / int_size)
        gc_collect_end()
    }
        
Based on these observations, I hereby conclude:

* `gc_collect()` has 3 steps: `gc_collect_start()`, `gc_collect_root(stack_boundary, stack_size)`, and `gc_collect_end()`

* Root pointers may not only stay in the stack, but also in registers, so registers should be copied to the stack

### How to add a module
1. Create a file `unix/modawesome.c`.

```C
    // unix/modawesome.c
    // This is the file for my awesome module in MicroPython.
    
    #include "py/runtime.h"
    
    STATIC mp_obj_t mod_awesome_impressive(void) {
    	return mp_obj_new_int(0);
    }
    STATIC MP_DEFINE_CONST_FUN_OBJ_0(mod_awesome_impressive_obj, mod_awesome_impressive);
    
    STATIC const mp_map_elem_t mp_module_awesome_globals_table[] = {
    	{ MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_OBJ_NEW_QSTR(MP_QSTR_awesome) },
    	{ MP_OBJ_NEW_QSTR(MP_QSTR_impressive), (mp_obj_t)&mod_awesome_impressive_obj },
    };
    
    STATIC MP_DEFINE_CONST_DICT(mp_module_awesome_globals, mp_module_awesome_globals_table);
    
    const mp_obj_module_t mp_module_awesome = {
    	.base = { &mp_type_module },
    	.name = MP_QSTR_awesome,
    	.globals = (mp_obj_dict_t*)&mp_module_awesome_globals,
    };
```

2. Open file `unix/qstrdefsport.h`, and add the following 2 lines.

```C
    Q(awesome)
    Q(impressive)
```

3. Open file `unix/mpconfigport.h`, and add the following line.

```C
    extern const struct _mp_obj_module_t mp_module_awesome;
```

4. Still in file `unix/mpconfigport.h`, modify `#define MICROPY_PORT_BUILTIN_MODULES` to include another line:

```C
    { MP_OBJ_NEW_QSTR(MP_QSTR_awesome), (mp_obj_t)&mp_module_awesome } \
```

5. Make and run.

### DE0 Module
This is a MicroPython module for Altera DE0-NANO-SOC board. See `de0/` for more detail.
