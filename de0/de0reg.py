from de0.de0mem_py import *

class Reg(object):
    def __init__(self, pa):
        
        self.pa = pa

    def set(self, v):
        write_uint32_to_pa(self.pa, v)

    def get(self):
        return read_uint32_from_pa(self.pa)

    def set_bit(self, bit):
        if bit > 31 or bit < 0:
            raise RuntimeError("bit must be in [0, 32).")
        mask = self.get() | (1 << bit)
        self.set(mask)

    def clear_bit(self, bit):
        if bit > 31 or bit < 0:
            raise RuntimeError("bit must be in [0, 32).")
        mask = self.get() & (~(1 << bit))
        self.set(mask)

    def get_bit(self, bit):
        if bit > 31 or bit < 0:
            raise RuntimeError("bit must be in [0, 32).")        
        return bool(self.get() & (1 << bit))
		