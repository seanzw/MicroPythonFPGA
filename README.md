# MicroPythonFPGA

This is a MicroPython port for the Altera DE0 Nano HPS-FPGA board. It runs on Linux, on the ARM processor in the HPS part of the board. This port adds several functionalities to support HPS-FPGA communication and control HPS peripherals.

## Getting the board ready
This port runs on Linux, in order to take advantage of what the OS can offer: file system, memory mapping, networking, ...

So, the first step is to configure the board so that it boots into Linux.

Download the [System CD](http://www.terasic.com.tw/cgi-bin/page/archive.pl?Language=English&No=593&PartNo=4) from Altera's official website. Inside the archive, you can find `Manual/DE0-Nano-SoC_Getting_Started_Guide.pdf`. Follow the instruction inside, and make sure you are able to do the following:

* Boot the board into Linux
* Connect the board through UART to your computer

Note that the SD card on the board should already have a Linux installed when it's shipped. But if it doesn't, or if you happen to have corrupted the SD card, you can always burn an image file to the card. To do so, follow the "Getting Started Guide". You need to use the pre-built image file Altera offers, for it has drivers for the peripherals.

Also note that simply trying to get the board running might take some work, especially if you are unlucky, so please be patient.

## Building MicroPython
Since we need to run MicroPython on the board, which has a 32-bit ARM processor, we need to cross-compile it for the platform.

You **must** compile this port inside Linux, for some Linux-specific feature is used. It is recommended that you run a 32-bit Linux. Note that in this process, no Altera specific tool is needed - all we need are standard tools.

First, clone the [official MicroPython GitHub repository](https://github.com/micropython/micropython) to your computer. You can do so by typing the following command:

```
git clone https://github.com/micropython/micropython
```

Get into the `micropython` directory:

```
cd micropython
```

You can see a lot of folders, many of which are different ports. The build process for each port is as follows:

* Go to the directory of a port, e.g. /unix
* Run `make` in that directory.

You might want to try this process by compiling the `unix` port. The `unix` port doesn't require a cross compiler, and it runs on a normal x86 PC.

Next, clone the [MicroPythonFPGA GitHub repositoy](https://github.com/seanzw/MicroPythonFPGA) into the directory in which MicroPython is stored. You can do so by typing the following command:

```
git clone https://github.com/seanzw/MicroPythonFPGA
```

Now your directory would look like this:

```
micropython
          |- unix
          |- unix-cpy
          |- MicroPythonFPGA
          ...
```

Get into the directory `MicroPythonFPGA` by typing

```
cd MicroPythonFPGA
```

Currently you can not `make`, since you don't have the cross compiler. Now install the cross compiler. Type the following command to install `gcc` for Linux on ARM:

```
sudo apt-get install gcc-arm-linux-gnueabihf
```

MicroPython uses `libffi`, so you also need to install this package. However, you can't simply `apt-get` it, for that would give you the x86 `libffi`. You need to cross compile an ARM version of `libffi`.

```
wget ftp://sourceware.org/pub/libffi/libffi-3.0.13.tar.gz
tar -xzf libffi-3.0.13.tar.gz
cd libffi-3.0.13/
./configure --host=arm-linux-gnueabihf --prefix=/usr/arm-linux-gnueabi hf
make
sudo make install
```

After installing the cross compiler and `libffi`, you can now run `make` inside `MicroPythonFPGA`.

You will get an executable file `micropython` in the current directory. You cannot run it on your computer, since it's for the board.

## Moving the MicroPython binary to the board
Now that we've compiled MicroPython, let's try it on the board.

Put the SD card into your card reader and you should be able to see a FAT disk partition (if you can see more, that's fine). Copy the following to that partition:

```
micropython (the executable)
de0 (the folder)
fft (the folder)
led (the folder)
```

Now put the SD card back on the board, and power on.

At this moment, you can't see `micropython` anywhere, since it's in the FAT partition. You need to mount that partition in order to access it.

```
mount /dev/mmcblk0p1 /mnt
cd /mnt
```

The commands above mounts the partition to the directory `/mnt`.

Now that you can see the FAT partition. Go to where you stored `micropython` before and run it.

```
./micropython
```

If you can see something like this:

```
Micro Python 35b48ff on 2015-08-27; linux version
>>> 
```

then congratulations! You are running MicroPython!

## Example 1: GSensor
Now let's do some demonstrations. This port of MicroPython adds some features for the DE0 board. We hope that through these demos, you can see that using Python makes developing a lot easier.

Our first example is the GSensor. This example mimics the demonstration offered in the "System CD", but it is written in MicroPython instead of C.

Inside the MicroPython prompt, type:

```
import de0
g = de0.GSensor()
g.XYZ_read()
```

and you would get something like:

```
[2, -19, 225]
```

This result is scaled. You need to multiply 4 to each number to get a measure of mg. So what the GSensor tells us is actually:

```
Gx = 8 mg, Gy = -76 mg, Gz = 900 mg
```

## Example 2: HPS LED
The last example only shows that we can read from peripherals. In this example, we can actually control one. 

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
