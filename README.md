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
git clone --recursive https://github.com/micropython/micropython
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
> This example is derived from the GSensor example in "System CD".

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

> This example is derived from the GPIO example in "System CD".

The last example only shows that we can read from peripherals. In this example, we can actually control one.

The HPS part of the board offers an LED that you can control without FPGA cooperation.

Inside the MicroPython prompt, type:

```
import de0
l = de0.HPS_LED()
l.status()
```

You should see `False`.

```
l.toggle()
```

You will find that an LED on the board is on.

`de0.HPS_LED` is a class which contains the following methods:

```
# Check whether the LED is currently on
status(): bool

# Switch on the LED. If it's already on, keep it on.
on()

# Switch off the LED. If it's already off, keep it off.
off()

# Switch the status of the LED.
toggle()
```

## Example 3: FPGA LED

> This example is derived from the FPGA LED example in "System CD".

Our next example is more complicated. We're going to communicate with the FPGA part of the board.

There are several ways to configure the FPGA.

### Configure FPGA in the booting process
If you are using the SD card image mentioned before, then inside the SD card root directory, you can find a file `de0_nano_soc.rbf`. The booting process is configured to automatically read this file and burn it into the FPGA. Needless to say, if we replace this file by our own image, we can load our FPGA image. Note that the image file **must** be an `.rbf` file. Copy `/led/HPS_CONTROL_FPGA_LED.rbf` to the root directory of the SD card, and rename it to `de0_nano_soc.rbf `.

If you are not using this SD card image, you can still configure the FPGA in the booting process. Refer to [this link](http://rocketboards.org/foswiki/view/Documentation/GSRD131ProgrammingFPGA) for how to do it.

### Configure FPGA by burning an image file inside Linux
After booting into Linux on the board, you can use the `dd` command to load an image file. To do it in this way, you need to make sure that after booting, the FPGA is still in a `configuration phase`. If you deleted the `de0_nano_soc.rbf` file in the root directory, the booting process would not be able to configure the FPGA, leaving it in a `configuration phase`.

After booting into Linux, type the following command:

```
dd if=your_image_file.rbf of=/dev/fpga0 bs=1M
```

If you see something like this:

```
4+1 records in
4+1 records out
```

then you're done!

### Configure FPGA by using Quartus through your computer
Power on the board. This time, connect not only the UART, but also "USB Blaster II" to your computer. We need to configure the FPGA through this.

Refer to the "Getting Started Guide" inside the "System CD" and follow the instructions in the chapter "Performing a FPGA System Test". The image file you need is `/led/HPS_CONTROL_FPGA_LED.sof`.

Note that to configure the FPGA in this way, you need to make sure:

* Start burning the image **after** booting. Each time the board boots, it loses the FPGA configuration.
* The image file is a `.sof` file instead of a `.rbf` file.

### Tesing the FPGA LED
After configuring the FPGA, a connection between HPS and FPGA is established. Now run MicroPython, and inside the prompt, type:

```
import led.test
```

You can see that several LEDs on the board are switching on and off in a certain fashion.

### Control the FPGA LED
You can control the FPGA LEDs just in the same fashion as controlling the HPS LED.

```
from led import *
l = de0led.LED(0)
l.toggle()
```

Note that there are 8 FPGA LEDs, so that you need to put an index parameter to get an LED instance.

## Example 4: FFT

> This example is derived from the FFT example on [rocketboard](http://rocketboards.org/foswiki/view/Documentation/WS1IntroToAlteraSoCDevices).

Our last example is a pretty decent application: FFT. It is also a joint work of HPS and FPGA.

To configure the FPGA, use the same method given in example 3. The image file you need is `/fft/fft.rbf` or `/fft/fft.sof`.

Inside the MicroPython prompt, you can run the FFT application by:

```
import fft.fft
```

You would get something like this:

```
fft = 7b 0 0
fft = 7c 4095 41581
fft = 7d 0 0
fft = 7e 0 0
fft = 7f 0 0
```

## Programming HPS-FPGA applications with MicroPython
If you want to build an actual application, you need to let the HPS and FPGA parts communicate. This is based on memory mapping.

### h2py.py

According to the "My First HPS FPGA" manual inside the "System CD", after configuring the connections between HPS and FPGA, you'll be able to generate header files for your C program. These header files contain a bunch of (physical) memory addresses, reading and writing to these addresses would accomplish the communication.

If you look at `hps_0.h` in the FPGA LED example on the "System CD", you can see that each component is defined in a clean format. We offer a tool to convert this kind of header file into `.py` files. Inside `MicroPythonFPGA/h2py` you can find `h2py.py`. Type command:

```
python h2py.py hps_0.h
```

and the script would generate `hps_0.py`. So you can refer to certain addresses in python by something like `LED_PIO.BASE`, instead of in C by something like `LED_PIO_BASE`.

### Automatic memory mapping

The addresses given in these header files are all physical addresses. If you want to visit such an address, you would first need to map it to a virtual address, with the `mmap` syscall in Linux.

Inside the `de0` module, we provide an automatic memory mapping functionality. Inside the MicroPython prompt, you can first type:

```
import de0
```

and then use

```
de0.write_int32_to_pa(pa, value)
```

to write a 32-bit integer `value` to physical address `pa`. The `de0` module maintains a mapping table behind the scene so that you don't have to worry about `mmap`.
