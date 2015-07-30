#
TARGET = HPS_CONTROL_FPGA_LED
SOCEDS_DEST_ROOT= /home/sean/altera/15.0/embedded
#
CROSS_COMPILE = arm-linux-gnueabihf-
CFLAGS = -g -Wall  -I${SOCEDS_DEST_ROOT}/ip/altera/hps/altera_hps/hwlib/include \
	-I${SOCEDS_DEST_ROOT}/ip/altera/hps/altera_hps/hwlib/include/soc_cv_av -Dsoc_cv_av
LDFLAGS =  -g -Wall  
CC = $(CROSS_COMPILE)gcc
# ARCH= arm


build: $(TARGET)
$(TARGET): main.o led.o
	$(CC) $(LDFLAGS)   $^ -o $@  
%.o : %.c
	$(CC) $(CFLAGS) -c $< -o $@

.PHONY: clean
clean:
	rm -f $(TARGET) *.a *.o *~ 
