from de0adxl345_c import *

XL345_RATE_3200     = 0x0f
XL345_RATE_1600     = 0x0e
XL345_RATE_800      = 0x0d
XL345_RATE_400      = 0x0c
XL345_RATE_200      = 0x0b
XL345_RATE_100      = 0x0a
XL345_RATE_50       = 0x09
XL345_RATE_25       = 0x08
XL345_RATE_12_5     = 0x07
XL345_RATE_6_25     = 0x06
XL345_RATE_3_125    = 0x05
XL345_RATE_1_563    = 0x04
XL345_RATE__782     = 0x03
XL345_RATE__39      = 0x02
XL345_RATE__195     = 0x01
XL345_RATE__098     = 0x00

XL345_RANGE_2G           = 0x00
XL345_RANGE_4G           = 0x01
XL345_RANGE_8G           = 0x02
XL345_RANGE_16G          = 0x03
XL345_DATA_JUST_RIGHT    = 0x00
XL345_DATA_JUST_LEFT     = 0x04
XL345_10BIT              = 0x00
XL345_FULL_RESOLUTION    = 0x08
XL345_INT_LOW            = 0x20
XL345_INT_HIGH           = 0x00
XL345_SPI3WIRE           = 0x40
XL345_SPI4WIRE           = 0x00
XL345_SELFTEST           = 0x80

XL345_OVERRUN            = 0x01
XL345_WATERMARK          = 0x02
XL345_FREEFALL           = 0x04
XL345_INACTIVITY         = 0x08
XL345_ACTIVITY           = 0x10
XL345_DOUBLETAP          = 0x20
XL345_SINGLETAP          = 0x40
XL345_DATAREADY          = 0x80

XL345_WAKEUP_8HZ           = 0x00
XL345_WAKEUP_4HZ           = 0x01
XL345_WAKEUP_2HZ           = 0x02
XL345_WAKEUP_1HZ           = 0x03
XL345_SLEEP                = 0x04
XL345_MEASURE              = 0x08
XL345_STANDBY              = 0x00
XL345_AUTO_SLEEP           = 0x10
XL345_ACT_INACT_SERIAL     = 0x20
XL345_ACT_INACT_CONCURRENT = 0x00

ADXL345_REG_DEVID       = 0x00
ADXL345_REG_POWER_CTL   = 0x2D
ADXL345_REG_DATA_FORMAT = 0x31
ADXL345_REG_FIFO_CTL    = 0x38
ADXL345_REG_BW_RATE     = 0x2C
ADXL345_REG_INT_ENALBE  = 0x2E # default value: 0x00
ADXL345_REG_INT_MAP     = 0x2F # default value: 0x00
ADXL345_REG_INT_SOURCE  = 0x30 # default value: 0x02
ADXL345_REG_DATA_FORMAT = 0x31 # defuault value: 0x00
ADXL345_REG_DATAX0      = 0x32 # read only
ADXL345_REG_DATAX1      = 0x33 # read only
ADXL345_REG_DATAY0      = 0x34 # read only
ADXL345_REG_DATAY1      = 0x35 # read only
ADXL345_REG_DATAZ0      = 0x36 # read only
ADXL345_REG_DATAZ1      = 0x37 # read only