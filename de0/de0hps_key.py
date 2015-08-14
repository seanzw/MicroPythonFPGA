from de0.de0gpio1 import GPIO1

BIT_HPS_KEY = 25

class HPS_KEY:

    def status(self):
        return GPIO1.EXT_PORTA.get_bit(BIT_HPS_KEY)
