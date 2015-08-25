from de0.de0mem_py import *

#######################################################
## The following definitions are pulled from csr_regs.h
#######################################################

CSR_STATUS_REG = 0x0
CSR_CONTROL_REG = 0x4
CSR_DESCRIPTOR_FILL_LEVEL_REG = 0x8
CSR_RESPONSE_FILL_LEVEL_REG = 0xC
CSR_SEQUENCE_NUMBER_REG = 0x10 # this register only exists when the enhanced features are enabled

# masks for the status register bits
CSR_BUSY_MASK = 1
CSR_BUSY_OFFSET = 0
CSR_DESCRIPTOR_BUFFER_EMPTY_MASK = 1 << 1
CSR_DESCRIPTOR_BUFFER_EMPTY_OFFSET = 1
CSR_DESCRIPTOR_BUFFER_FULL_MASK = 1 << 2
CSR_DESCRIPTOR_BUFFER_FULL_OFFSET = 2
CSR_RESPONSE_BUFFER_EMPTY_MASK = 1 << 3
CSR_RESPONSE_BUFFER_EMPTY_OFFSET = 3
CSR_RESPONSE_BUFFER_FULL_MASK = 1 << 4
CSR_RESPONSE_BUFFER_FULL_OFFSET = 4
CSR_STOP_STATE_MASK = 1 << 5
CSR_STOP_STATE_OFFSET = 5
CSR_RESET_STATE_MASK = 1 << 6
CSR_RESET_STATE_OFFSET = 6
CSR_STOPPED_ON_ERROR_MASK = 1 << 7
CSR_STOPPED_ON_ERROR_OFFSET = 7
CSR_STOPPED_ON_EARLY_TERMINATION_MASK = 1 << 8
CSR_STOPPED_ON_EARLY_TERMINATION_OFFSET = 8
CSR_IRQ_SET_MASK = 1 << 9
CSR_IRQ_SET_OFFSET = 9

# masks for the control register bits
CSR_STOP_MASK = 1
CSR_STOP_OFFSET = 0
CSR_RESET_MASK = 1 << 1
CSR_RESET_OFFSET = 1
CSR_STOP_ON_ERROR_MASK = 1 << 2
CSR_STOP_ON_ERROR_OFFSET = 2
CSR_STOP_ON_EARLY_TERMINATION_MASK = 1 << 3
CSR_STOP_ON_EARLY_TERMINATION_OFFSET = 3
CSR_GLOBAL_INTERRUPT_MASK = 1 << 4
CSR_GLOBAL_INTERRUPT_OFFSET = 4
CSR_STOP_DESCRIPTORS_MASK = 1 << 5
CSR_STOP_DESCRIPTORS_OFFSET = 5

# masks for the FIFO fill levels and sequence number
CSR_READ_FILL_LEVEL_MASK = 0xFFFF
CSR_READ_FILL_LEVEL_OFFSET = 0
CSR_WRITE_FILL_LEVEL_MASK = 0xFFFF0000
CSR_WRITE_FILL_LEVEL_OFFSET = 16
CSR_RESPONSE_FILL_LEVEL_MASK = 0xFFFF
CSR_RESPONSE_FILL_LEVEL_OFFSET = 0
CSR_READ_SEQUENCE_NUMBER_MASK = 0xFFFF
CSR_READ_SEQUENCE_NUMBER_OFFSET = 0
CSR_WRITE_SEQUENCE_NUMBER_MASK = 0xFFFF0000
CSR_WRITE_SEQUENCE_NUMBER_OFFSET = 16

# read/write macros for each 32 bit register of the CSR port
def WR_CSR_STATUS(base, data):
    write_uint32_to_pa(base + CSR_STATUS_REG, data)
    
def WR_CSR_CONTROL(base, data):
    write_uint32_to_pa(base + CSR_CONTROL_REG, data)
    
def RD_CSR_STATUS(base):
    return read_uint32_from_pa(base + CSR_STATUS_REG)
    
def RD_CSR_CONTROL(base):
    return read_uint32_from_pa(base + CSR_CONTROL_REG)
    
def RD_CSR_DESCRIPTOR_FILL_LEVEL(base):
    return read_uint32_from_pa(base + CSR_DESCRIPTOR_FILL_LEVEL_REG)
    
def RD_CSR_RESPONSE_FILL_LEVEL(base):
    return read_uint32_from_pa(base+ CSR_RESPONSE_FILL_LEVEL_REG)
    
def RD_CSR_SEQUENCE_NUMBER(base):
    return read_uint32_from_pa(base+ CSR_SEQUENCE_NUMBER_REG)


##############################################################
## The following definitions are pulled from descriptor_regs.h
##############################################################
#  Descriptor formats:
#
#  Standard Format:
#  
#  Offset         |             3                 2                 1                   0
#  --------------------------------------------------------------------------------------
#   0x0           |                              Read Address[31..0]
#   0x4           |                              Write Address[31..0]
#   0x8           |                                Length[31..0]
#   0xC           |                                Control[31..0]
#
#  Extended Format:
#  
#  Offset         |               3                           2                           1                          0
#  -------------------------------------------------------------------------------------------------------------------
#   0x0           |                                                  Read Address[31..0]
#   0x4           |                                                  Write Address[31..0]
#   0x8           |                                                    Length[31..0]
#   0xC           |      Write Burst Count[7..0]  |  Read Burst Count[7..0]  |           Sequence Number[15..0]
#   0x10          |                      Write Stride[15..0]                 |              Read Stride[15..0]
#   0x14          |                                                  Read Address[63..32]
#   0x18          |                                                  Write Address[63..32]
#   0x1C          |                                                     Control[31..0]
#
#  Note:  The control register moves from offset 0xC to 0x1C depending on the format used

DESCRIPTOR_READ_ADDRESS_REG = 0x0
DESCRIPTOR_WRITE_ADDRESS_REG = 0x4
DESCRIPTOR_LENGTH_REG = 0x8
DESCRIPTOR_CONTROL_STANDARD_REG = 0xC
DESCRIPTOR_SEQUENCE_NUMBER_REG = 0xC
DESCRIPTOR_READ_BURST_REG = 0xE
DESCRIPTOR_WRITE_BURST_REG = 0xF
DESCRIPTOR_READ_STRIDE_REG = 0x10
DESCRIPTOR_WRITE_STRIDE_REG = 0x12
DESCRIPTOR_READ_ADDRESS_HIGH_REG = 0x14
DESCRIPTOR_WRITE_ADDRESS_HIGH_REG = 0x18
DESCRIPTOR_CONTROL_ENHANCED_REG = 0x1C

# masks and offsets for the sequence number and programmable burst counts
DESCRIPTOR_SEQUENCE_NUMBER_MASK = 0xFFFF
DESCRIPTOR_SEQUENCE_NUMBER_OFFSET = 0
DESCRIPTOR_READ_BURST_COUNT_MASK = 0x00FF0000
DESCRIPTOR_READ_BURST_COUNT_OFFSET = 16
DESCRIPTOR_WRITE_BURST_COUNT_MASK = 0xFF000000
DESCRIPTOR_WRITE_BURST_COUNT_OFFSET = 24

# masks and offsets for the read and write strides
DESCRIPTOR_READ_STRIDE_MASK = 0xFFFF
DESCRIPTOR_READ_STRIDE_OFFSET = 0
DESCRIPTOR_WRITE_STRIDE_MASK = 0xFFFF0000
DESCRIPTOR_WRITE_STRIDE_OFFSET = 16

# masks and offsets for the bits in the descriptor control field
DESCRIPTOR_CONTROL_TRANSMIT_CHANNEL_MASK = 0xFF
DESCRIPTOR_CONTROL_TRANSMIT_CHANNEL_OFFSET = 0
DESCRIPTOR_CONTROL_GENERATE_SOP_MASK = 1 << 8
DESCRIPTOR_CONTROL_GENERATE_SOP_OFFSET = 8
DESCRIPTOR_CONTROL_GENERATE_EOP_MASK = 1 << 9
DESCRIPTOR_CONTROL_GENERATE_EOP_OFFSET = 9
DESCRIPTOR_CONTROL_PARK_READS_MASK = 1 << 10
DESCRIPTOR_CONTROL_PARK_READS_OFFSET = 10
DESCRIPTOR_CONTROL_PARK_WRITES_MASK = 1 << 11
DESCRIPTOR_CONTROL_PARK_WRITES_OFFSET = 11
DESCRIPTOR_CONTROL_END_ON_EOP_MASK = 1 << 12
DESCRIPTOR_CONTROL_END_ON_EOP_OFFSET = 12
DESCRIPTOR_CONTROL_TRANSFER_COMPLETE_IRQ_MASK = 1 << 14
DESCRIPTOR_CONTROL_TRANSFER_COMPLETE_IRQ_OFFSET = 14
DESCRIPTOR_CONTROL_EARLY_TERMINATION_IRQ_MASK = 1 << 15
DESCRIPTOR_CONTROL_EARLY_TERMINATION_IRQ_OFFSET = 15
DESCRIPTOR_CONTROL_ERROR_IRQ_MASK = 0xFF << 16 # the read master will use this as the transmit error, the dispatcher will use this to generate an interrupt if any of the error bits are asserted by the write master
DESCRIPTOR_CONTROL_ERROR_IRQ_OFFSET = 16
DESCRIPTOR_CONTROL_EARLY_DONE_ENABLE_MASK = 1 << 24
DESCRIPTOR_CONTROL_EARLY_DONE_ENABLE_OFFSET = 24
DESCRIPTOR_CONTROL_GO_MASK = 1 << 31 # at a minimum you always have to write '1' to this bit as it commits the descriptor to the dispatcher
DESCRIPTOR_CONTROL_GO_OFFSET = 31

# Each register is byte lane accessible so the some of the values that are
# less than 32 bits wide are written to according to the field width.
def WR_DESCRIPTOR_READ_ADDRESS(base, data):
    write_uint32_to_pa(base + DESCRIPTOR_READ_ADDRESS_REG, data)
    
def WR_DESCRIPTOR_WRITE_ADDRESS(base, data):
    write_uint32_to_pa(base + DESCRIPTOR_WRITE_ADDRESS_REG, data)
    
def WR_DESCRIPTOR_LENGTH(base, data):
    write_uint32_to_pa(base + DESCRIPTOR_LENGTH_REG, data)
    
def WR_DESCRIPTOR_CONTROL_STANDARD(base, data):
    write_uint32_to_pa(base + DESCRIPTOR_CONTROL_STANDARD_REG, data) # this pushes the descriptor into the read/write FIFOs when standard descriptors are used
    
def WR_DESCRIPTOR_SEQUENCE_NUMBER(base, data):
    write_uint32_to_pa(base + DESCRIPTOR_SEQUENCE_NUMBER_REG, data)
    
def WR_DESCRIPTOR_READ_BURST(base, data):
    write_uint32_to_pa(base + DESCRIPTOR_READ_BURST_REG, data)
    
def WR_DESCRIPTOR_WRITE_BURST(base, data):
    write_uint32_to_pa(base + DESCRIPTOR_WRITE_BURST_REG, data)
    
def WR_DESCRIPTOR_READ_STRIDE(base, data):
    write_uint32_to_pa(base + DESCRIPTOR_READ_STRIDE_REG, data)
    
def WR_DESCRIPTOR_WRITE_STRIDE(base, data):
    write_uint32_to_pa(base + DESCRIPTOR_WRITE_STRIDE_REG, data)
    
def WR_DESCRIPTOR_READ_ADDRESS_HIGH(base, data):
    write_uint32_to_pa(base + DESCRIPTOR_READ_ADDRESS_HIGH_REG, data)
    
def WR_DESCRIPTOR_WRITE_ADDRESS_HIGH(base, data):
    write_uint32_to_pa(base + DESCRIPTOR_WRITE_ADDRESS_HIGH_REG, data)
    
def WR_DESCRIPTOR_CONTROL_ENHANCED(base, data):
    write_uint32_to_pa(base + DESCRIPTOR_CONTROL_ENHANCED_REG, data) # this pushes the descriptor into the read/write FIFOs when the extended descriptors are used


############################################################
## The following definitions are pulled from response_regs.h
############################################################

RESPONSE_ACTUAL_BYTES_TRANSFERRED_REG = 0x0
RESPONSE_ERRORS_REG = 0x4

# bits making up the "errors" register
RESPONSE_ERROR_MASK = 0xFF
RESPONSE_ERROR_OFFSET = 0
RESPONSE_EARLY_TERMINATION_MASK = 1 << 8
RESPONSE_EARLY_TERMINATION_OFFSET = 8

# read macros for each 32 bit register
def RD_RESPONSE_ACTUAL_BYTES_TRANSFFERED(base):
    return read_uint32_from_pa(base + RESPONSE_ACTUAL_BYTES_TRANSFERRED_REG)
def RD_RESPONSE_ERRORS_REG(base):
    return read_uint32_from_pa(base + RESPONSE_ERRORS_REG)


######################################################################################
## The following definitions are pulled from sgdma_dispatcher.c and sgdma_dispatcher.h
######################################################################################

ENOSPC = 28  # No space left on device
ENODATA = 61 # No data available

class StandardDescriptor:
    def __init__(self, read_address, write_address, length, control):
        self.read_address = read_address
        self.write_address = write_address
        self.transfer_length = length
        self.control = control
        
    def write(self, csr_base, descriptor_base):
        if ((RD_CSR_STATUS(csr_base) & CSR_DESCRIPTOR_BUFFER_FULL_MASK) != 0):
            return -ENOSPC # at least one descriptor buffer is full, returning so that this function is non-blocking
  
        WR_DESCRIPTOR_READ_ADDRESS(descriptor_base, self.read_address);
        WR_DESCRIPTOR_WRITE_ADDRESS(descriptor_base, self.write_address);
        WR_DESCRIPTOR_LENGTH(descriptor_base, self.transfer_length);
        WR_DESCRIPTOR_CONTROL_STANDARD(descriptor_base, self.control);
        return 0

def construct_standard_st_to_mm_descriptor(write_address, length, control):
    return StandardDescriptor(0, write_address, length, control | DESCRIPTOR_CONTROL_GO_MASK)
    
def construct_standard_mm_to_st_descriptor(read_address, length, control):
    return StandardDescriptor(read_address, 0, length, control | DESCRIPTOR_CONTROL_GO_MASK)
    
def construct_standard_mm_to_mm_descriptor(read_address, write_address, length, control):
    return StandardDescriptor(read_address, write_address, length, control | DESCRIPTOR_CONTROL_GO_MASK)
    
def read_csr_status(csr_base):
    return RD_CSR_STATUS(csr_base)