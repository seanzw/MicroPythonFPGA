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

class StandardDescriptor:
    def __init__(self, read_address, write_address, length, control):
        self.read_address = read_address
        self.write_address = write_address
        self.transfer_length = length
        self.control = control

def construct_standard_st_to_mm_descriptor(write_address, length, control):
    return StandardDescriptor(0, write_address, length, control | DESCRIPTOR_CONTROL_GO_MASK)