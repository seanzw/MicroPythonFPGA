import hps_0 as HPS_0
from sgdma_dispatcher import *
from de0.de0mem_py import *

ALT_LWFPGASLVS_OFST = 0xFF200000
mmapedBase = ALT_LWFPGASLVS_OFST

DATA_BASE = HPS_0.FFT_SUB_DATA.BASE + mappedBase
for i in range(0, data_length):
	temp = 0x7fff if ((i % 32) < 16) else 0x8000
	write_uint32_to_pa(DATA_BASE + i * 4, temp)
	print("signal 0x%X %d" % (i, temp))

RESULT_BASE = HPS_0.FFT_SUB_DATA.BASE + mappedBase + HPS_0.FFT_SUB_DATA.SPAN // 2
for i in range(0, data_length * 2):
	write_uint32_to_pa(RESULT_BASE + i * 4, 0) # zero out result
	
# tell the FFT how long the fft is
FFT_CSR_BASE = mappedBase + HPS_0.FFT_SUB_FFT_STADAPTER_0.BASE
write_uint32_to_pa(FFT_CSR_BASE, data_length)

DMA_DATA_BASE = HPS_0.FFT_SUB_SGDMA_FROM_FFT_FFT_SUB_DATA.BASE
descriptor0 = construct_standard_mm_to_st_descriptor(
	DMA_DATA_BASE,
	data_length * 4,
	DESCRIPTOR_CONTROL_GENERATE_SOP_MASK | DESCRIPTOR_CONTROL_GENERATE_EOP_MASK
)

DMA_RESULT_BASE = HPS_0.FFT_SUB_SGDMA_FROM_FFT_FFT_SUB_DATA.BASE + HPS_0.FFT_SUB_SGDMA_FROM_FFT_FFT_SUB_DATA.SPAN // 2
descriptor1 = construct_standard_st_to_mm_descriptor(
	DMA_RESULT_BASE,
	data_length * 8,
	DESCRIPTOR_CONTROL_END_ON_EOP_MASK
)

SGDMA_TO_FFT_CSR_BASE = mappedBase + HPS_0.FFT_SUB_SGDMA_TO_FFT_CSR.BASE
SGDMA_TO_FFT_DESCRIPTOR_SLAVE_BASE = mappedBase + HPS_0.FFT_SUB_SGDMA_TO_FFT_DESCRIPTOR_SLAVE.BASE
descriptor0.write(
	SGDMA_TO_FFT_CSR_BASE,
	SGDMA_TO_FFT_DESCRIPTOR_SLAVE_BASE
)

SGDMA_FROM_FFT_CSR_BASE = mappedBase + HPS_0.FFT_SUB_SGDMA_FROM_FFT_CSR.BASE
SGDMA_FROM_FFT_DESCRIPTOR_SLAVE_BASE = mappedBase + HPS_0.FFT_SUB_SGDMA_FROM_FFT_DESCRIPTOR_SLAVE.BASE
descriptor1.write(
	SGDMA_FROM_FFT_CSR_BASE,
	SGDMA_FROM_FFT_DESCRIPTOR_SLAVE_BASE
)

print("Waiting for result...")
while read_csr_status(SGDMA_TO_FFT_CSR_BASE) != 2:
	pass
while read_csr_status(SGDMA_FROM_FFT_CSR_BASE) != 2:
	pass

for i in range(0, data_length):
	real = read_uint32_from_pa(RESULT_BASE + 2 * i * 4)
	image = read_uint32_from_pa(RESULT_BASE + (2 * i + 1) * 4)
	print("fft = %x %d %d" % (i, real, image))
