import de0.de0adxl345_py as adxl

class GSensor:
    fd = -1

    def __init__(self):
        if GSensor.fd == -1:
            GSensor.fd = adxl.init()

        adxl.reg_write(GSensor.fd, adxl.ADXL345_REG_DATA_FORMAT, adxl.XL345_RANGE_2G | adxl.XL345_FULL_RESOLUTION)
        adxl.reg_write(GSensor.fd, adxl.ADXL345_REG_BW_RATE, adxl.XL345_RATE_50)
        adxl.reg_write(GSensor.fd, adxl.ADXL345_REG_INT_ENALBE, adxl.XL345_DATAREADY)
        adxl.reg_write(GSensor.fd, adxl.ADXL345_REG_POWER_CTL, adxl.XL345_STANDBY)
        adxl.reg_write(GSensor.fd, adxl.ADXL345_REG_POWER_CTL, adxl.XL345_MEASURE)

    def is_data_ready(self):
        data = adxl.reg_read(GSensor.fd, adxl.ADXL345_REG_INT_SOURCE)
        return bool(data & adxl.XL345_DATAREADY)

    def XYZ_read(self):
        data = adxl.reg_multi_read(GSensor.fd, 0x32, 6)
        ret = [data[1] << 8 | data[0], data[3] << 8 | data[2], data[5] << 8 | data[4]]
        return [x - 65536 if bool(x & (1 << 15)) else x for x in ret]

    def Id_read(self):
        return adxl.reg_read(GSensor.fd, adxl.ADXL345_REG_DEVID)