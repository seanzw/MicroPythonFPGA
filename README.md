# MicroPythonFPGA

## RocketBoards Tutorials
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




