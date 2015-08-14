# Led python module based on de0mem
from de0.de0mem_py import *
import de0.hps_0 as hps_0

class led(object):
	"""led class"""
	
	def __init__(self, idx):
		super(led, self).__init__()
		
		if 'LED_PIO' not in dir(hps_0):
			raise RuntimeError('Cannot find "LED_PIO" in hps_0')
		__base__ = 0xFF200000 + hps_0.LED_PIO.BASE
		
		if idx > 7:
			self.idx = 7
		elif idx < 0:
			self.idx = 0
		else:
			self.idx = idx

	def on(self):
		mask = read_uint32_from_pa(led.__base__) | (1 << self.idx)
		write_uint32_to_pa(LED_PIO_BASE, mask)

	def off(self):
		mask = read_uint32_from_pa(led.__base__) & (~(1 << self.idx))
		write_uint32_to_pa(LED_PIO_BASE, mask)

	def status(self):
		return bool(read_uint32_from_pa(led.__base__) & (1 << self.idx))

	def toggle(self):
		if self.status():
			self.off()
		else:
			self.on()
