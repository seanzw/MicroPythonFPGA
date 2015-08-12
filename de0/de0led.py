# Led python module based on de0mem
from de0.de0mem_py import *
from de0.hps_0 import *

# LED_PIO_BASE = 0x10040 + 0xFF200000
LED_PIO_BASE = 0xFF200000 + LED_PIO.BASE

class led(object):
	"""led class"""
	def __init__(self, idx):
		super(led, self).__init__()
		if idx > 7:
			self.idx = 7
		elif idx < 0:
			self.idx = 0
		else:
			self.idx = idx

	def on(self):
		mask = read_uint32_from_pa(LED_PIO_BASE) | (1 << self.idx)
		write_uint32_to_pa(LED_PIO_BASE, mask)

	def off(self):
		mask = read_uint32_from_pa(LED_PIO_BASE) & (~(1 << self.idx))
		write_uint32_to_pa(LED_PIO_BASE, mask)

	def status(self):
		return bool(read_uint32_from_pa(LED_PIO_BASE) & (1 << self.idx))

	def toggle(self):
		if self.status():
			self.off()
		else:
			self.on()
