from de0.de0reg import Reg

class GPIO1():
    BASE = 0xFF709000
    SWPORTA_DR = Reg(BASE + 0x0)
    SWPORTA_DDR = Reg(BASE + 0x4)
    EXT_PORTA = Reg(BASE + 0x50)