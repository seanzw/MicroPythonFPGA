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

