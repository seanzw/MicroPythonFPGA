import led.de0led as led
import utime as ut

leds = [led.LED(i) for i in range(0, 8)]
for i in range(0, 16):
    leds[i % 8].toggle()
    ut.sleep(0.5)
