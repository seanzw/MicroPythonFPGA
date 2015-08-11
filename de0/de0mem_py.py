import de0mem_c

# (pa_begin, pa_nbytes, va_begin)
__ranges__ = [
    (0xFC000000, 0x4, -1), # ALT_STM
    (0xFF000000, 0x4, -1), # ALT_DAP
    (0xFF200000, 0x200000, -1), # ALT_LWFPGASLVS
    (0xFF400000, 0x80000, -1), # ALT_LWH2F
    (0xFF500000, 0x8000, -1), # ALT_H2F
    (0xFF600000, 0x80000, -1), # ALT_F2H
    (0xFF700000, 0x2000, -1), # ALT_EMAC0
    (0xFF702000, 0x2000, -1), # ALT_EMAC1
    (0xFF704000, 0x400, -1), # ALT_SDMMC
    (0xFF705000, 0x100, -1), # ALT_QSPI
    (0xFF706000, 0x1000, -1), # ALT_FPGAMGR
    (0xFF707000, 0x1000, -1), # ALT_ACPIDMAP
    (0xFF708000, 0x80, -1), # ALT_GPIO0
    (0xFF709000, 0x80, -1), # ALT_GPIO1
    (0xFF70A000, 0x80, -1), # ALT_GPIO2
    (0xFF800000, 0x80000, -1), # ALT_L3
    (0xFF900000, 0x100000, -1), # ALT_NANDDATA
    (0xFFA00000, 0x100000, -1), # ALT_QSPIDATA
    (0xFFB00000, 0x40000, -1), # ALT_USB0
    (0xFFB40000, 0x40000, -1), # ALT_USB1
    (0xFFB80000, 0x800, -1), # ALT_NAND
    (0xFFB90000, 0x4, -1), # ALT_FPGAMGRDATA
    (0xFFC00000, 0x200, -1), # ALT_CAN0
    (0xFFC01000, 0x200, -1), # ALT_CAN1
    (0xFFC02000, 0x100, -1), # ALT_UART0
    (0xFFC03000, 0x100, -1), # ALT_UART1
    (0xFFC04000, 0x100, -1), # ALT_I2C0
    (0xFFC05000, 0x100, -1), # ALT_I2C1
    (0xFFC06000, 0x100, -1), # ALT_I2C2
    (0xFFC07000, 0x100, -1), # ALT_I2C3
    (0xFFC08000, 0x100, -1), # ALT_SPTMR0
    (0xFFC09000, 0x100, -1), # ALT_SPTMR1
    (0xFFC20000, 0x20000, -1), # ALT_SDR
    (0xFFD00000, 0x100, -1), # ALT_OSC1TMR0
    (0xFFD01000, 0x100, -1), # ALT_OSC1TMR1
    (0xFFD02000, 0x100, -1), # ALT_L4WD0
    (0xFFD03000, 0x100, -1), # ALT_L4WD1
    (0xFFD04000, 0x200, -1), # ALT_CLKMGR
    (0xFFD05000, 0x100, -1), # ALT_RSTMGR
    (0xFFD08000, 0x4000, -1), # ALT_SYSMGR
    (0xFFE00000, 0x4, -1), # ALT_DMANONSECURE
    (0xFFE01000, 0x4, -1), # ALT_DMASECURE
    (0xFFE02000, 0x80, -1), # ALT_SPIS0
    (0xFFE03000, 0x80, -1), # ALT_SPIS1
    (0xFFF00000, 0x100, -1), # ALT_SPIM0
    (0xFFF01000, 0x100, -1), # ALT_SPIM1
    (0xFFF02000, 0x20, -1), # ALT_SCANMGR
    (0xFFFD0000, 0x10000, -1), # ALT_ROM
    (0xFFFEC000, 0x4, -1), # ALT_MPUSCU
    (0xFFFEF000, 0x4, -1), # ALT_MPUL2
    (0xFFFF0000, 0x10000, -1), # ALT_OCRAM
]

def __get_va__(pa):
    for idx in range(len(__ranges__)):
        (pa_begin, pa_nbytes, va_begin) = __ranges__[idx]
        
        # if pa falls inside [pa_begin, pa_begin + pa_nbytes)
        if pa >= pa_begin and pa - pa_begin < pa_nbytes:
            print("Physical address is in [%d, %d)" % (pa_begin, pa + pa_nbytes))
            
            # if not mapped yet
            if va_begin == -1:
                va_begin = de0mem_c.mmap(pa_begin, pa_nbytes)
                
                if va_begin < 0:
                    print("mmap failed, err = %d" % va_begin)
                    va_begin = -1
                    return -1
                    
                __ranges__[idx] = (pa_begin, pa_nbytes, va_begin)
            
            return va_begin + (pa - pa_begin)
            
    return -1
    
# write
def write_int8_to_pa(pa, val):
    va = __get_va__(pa)
    de0mem_c.write_int8_to_va(va, val)

def write_int16_to_pa(pa, val):
    va = __get_va__(pa)
    de0mem_c.write_int16_to_va(va, val)

def write_int32_to_pa(pa, val):
    va = __get_va__(pa)
    de0mem_c.write_int32_to_va(va, val)
    
def write_uint8_to_pa(pa, val):
    va = __get_va__(pa)
    de0mem_c.write_uint8_to_va(va, val)
    
def write_uint16_to_pa(pa, val):
    va = __get_va__(pa)
    de0mem_c.write_uint16_to_va(va, val)
    
def write_uint32_to_pa(pa, val):
    va = __get_va__(pa)
    de0mem_c.write_uint32_to_va(va, val)
    
# read
def read_int8_from_pa(pa):
    va = __get_va__(pa)
    return de0mem_c.read_int8_from_va(va)
    
def read_uint8_from_pa(pa):
    va = __get_va__(pa)
    return de0mem_c.read_uint8_from_va(va)
    
def read_int16_from_pa(pa):
    va = __get_va__(pa)
    return de0mem_c.read_int16_from_va(va)
    
def read_uint16_from_pa(pa):
    va = __get_va__(pa)
    return de0mem_c.read_uint16_from_va(va)
    
def read_int32_from_pa(pa):
    va = __get_va__(pa)
    return de0mem_c.read_int32_from_va(va)
    
def read_uint32_from_pa(pa):
    va = __get_va__(pa)
    return de0mem_c.read_uint32_from_va(va)
    
def what():
    print("what")
