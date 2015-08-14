from de0.de0gpio1 import GPIO1

BIT_HPS_LED = 24

class HPS_LED:

    def __set_direction__(self, direction):
        if direction:
            GPIO1.SWPORTA_DDR.set_bit(BIT_HPS_LED)
        else:
            GPIO1.SWPORTA_DDR.clear_bit(BIT_HPS_LED)

    def on(self):
        self.__set_direction__(True)
        GPIO1.SWPORTA_DR.set_bit(BIT_HPS_LED)

    def off(self):
        self.__set_direction__(True)
        GPIO1.SWPORTA_DR.clear_bit(BIT_HPS_LED)

    def status(self):
        self.__set_direction__(False)
        return GPIO1.SWPORTA_DR.get_bit(BIT_HPS_LED)

    def toggle(self):
        if self.status():
            self.off()
        else:
            self.on()
