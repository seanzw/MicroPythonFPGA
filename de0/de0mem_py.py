import de0mem_c as __de0mem_c__

ALT_STM = 0xFC000000 
ALT_DAP = 0xFF000000 
ALT_LWFPGASLVS = 0xFF200000 
ALT_LWH2F = 0xFF400000 
ALT_H2F = 0xFF500000 
ALT_F2H = 0xFF600000 
ALT_EMAC0 = 0xFF700000 
ALT_EMAC1 = 0xFF702000 
ALT_SDMMC = 0xFF704000 
ALT_QSPI = 0xFF705000 
ALT_FPGAMGR = 0xFF706000 
ALT_ACPIDMAP = 0xFF707000 
ALT_GPIO0 = 0xFF708000 
ALT_GPIO1 = 0xFF709000 
ALT_GPIO2 = 0xFF70A000 
ALT_L3 = 0xFF800000 
ALT_NANDDATA = 0xFF900000 
ALT_QSPIDATA = 0xFFA00000 
ALT_USB0 = 0xFFB00000 
ALT_USB1 = 0xFFB40000 
ALT_NAND = 0xFFB80000 
ALT_FPGAMGRDATA = 0xFFB90000 
ALT_CAN0 = 0xFFC00000 
ALT_CAN1 = 0xFFC01000 
ALT_UART0 = 0xFFC02000 
ALT_UART1 = 0xFFC03000 
ALT_I2C0 = 0xFFC04000 
ALT_I2C1 = 0xFFC05000 
ALT_I2C2 = 0xFFC06000 
ALT_I2C3 = 0xFFC07000 
ALT_SPTMR0 = 0xFFC08000 
ALT_SPTMR1 = 0xFFC09000 
ALT_SDR = 0xFFC20000 
ALT_OSC1TMR0 = 0xFFD00000 
ALT_OSC1TMR1 = 0xFFD01000 
ALT_L4WD0 = 0xFFD02000 
ALT_L4WD1 = 0xFFD03000 
ALT_CLKMGR = 0xFFD04000 
ALT_RSTMGR = 0xFFD05000 
ALT_SYSMGR = 0xFFD08000 
ALT_DMANONSECURE = 0xFFE00000 
ALT_DMASECURE = 0xFFE01000 
ALT_SPIS0 = 0xFFE02000 
ALT_SPIS1 = 0xFFE03000 
ALT_SPIM0 = 0xFFF00000 
ALT_SPIM1 = 0xFFF01000 
ALT_SCANMGR = 0xFFF02000 
ALT_ROM = 0xFFFD0000 
ALT_MPUSCU = 0xFFFEC000 
ALT_MPUL2 = 0xFFFEF000 
ALT_OCRAM = 0xFFFF0000 

# (pa_begin, pa_nbytes, va_begin)
__ranges__ = [
    (ALT_STM, 0x4, -1), # ALT_STM
    (ALT_DAP, 0x4, -1), # ALT_DAP
    (ALT_LWFPGASLVS, 0x200000, -1), # ALT_LWFPGASLVS
    (ALT_LWH2F, 0x80000, -1), # ALT_LWH2F
    (ALT_H2F, 0x8000, -1), # ALT_H2F
    (ALT_F2H, 0x80000, -1), # ALT_F2H
    (ALT_EMAC0, 0x2000, -1), # ALT_EMAC0
    (ALT_EMAC1, 0x2000, -1), # ALT_EMAC1
    (ALT_SDMMC, 0x400, -1), # ALT_SDMMC
    (ALT_QSPI, 0x100, -1), # ALT_QSPI
    (ALT_FPGAMGR, 0x1000, -1), # ALT_FPGAMGR
    (ALT_ACPIDMAP, 0x1000, -1), # ALT_ACPIDMAP
    (ALT_GPIO0, 0x80, -1), # ALT_GPIO0
    (ALT_GPIO1, 0x80, -1), # ALT_GPIO1
    (ALT_GPIO2, 0x80, -1), # ALT_GPIO2
    (ALT_L3, 0x80000, -1), # ALT_L3
    (ALT_NANDDATA, 0x100000, -1), # ALT_NANDDATA
    (ALT_QSPIDATA, 0x100000, -1), # ALT_QSPIDATA
    (ALT_USB0, 0x40000, -1), # ALT_USB0
    (ALT_USB1, 0x40000, -1), # ALT_USB1
    (ALT_NAND, 0x800, -1), # ALT_NAND
    (ALT_FPGAMGRDATA, 0x4, -1), # ALT_FPGAMGRDATA
    (ALT_CAN0, 0x200, -1), # ALT_CAN0
    (ALT_CAN1, 0x200, -1), # ALT_CAN1
    (ALT_UART0, 0x100, -1), # ALT_UART0
    (ALT_UART1, 0x100, -1), # ALT_UART1
    (ALT_I2C0, 0x100, -1), # ALT_I2C0
    (ALT_I2C1, 0x100, -1), # ALT_I2C1
    (ALT_I2C2, 0x100, -1), # ALT_I2C2
    (ALT_I2C3, 0x100, -1), # ALT_I2C3
    (ALT_SPTMR0, 0x100, -1), # ALT_SPTMR0
    (ALT_SPTMR1, 0x100, -1), # ALT_SPTMR1
    (ALT_SDR, 0x20000, -1), # ALT_SDR
    (ALT_OSC1TMR0, 0x100, -1), # ALT_OSC1TMR0
    (ALT_OSC1TMR1, 0x100, -1), # ALT_OSC1TMR1
    (ALT_L4WD0, 0x100, -1), # ALT_L4WD0
    (ALT_L4WD1, 0x100, -1), # ALT_L4WD1
    (ALT_CLKMGR, 0x200, -1), # ALT_CLKMGR
    (ALT_RSTMGR, 0x100, -1), # ALT_RSTMGR
    (ALT_SYSMGR, 0x4000, -1), # ALT_SYSMGR
    (ALT_DMANONSECURE, 0x4, -1), # ALT_DMANONSECURE
    (ALT_DMASECURE, 0x4, -1), # ALT_DMASECURE
    (ALT_SPIS0, 0x80, -1), # ALT_SPIS0
    (ALT_SPIS1, 0x80, -1), # ALT_SPIS1
    (ALT_SPIM0, 0x100, -1), # ALT_SPIM0
    (ALT_SPIM1, 0x100, -1), # ALT_SPIM1
    (ALT_SCANMGR, 0x20, -1), # ALT_SCANMGR
    (ALT_ROM, 0x10000, -1), # ALT_ROM
    (ALT_MPUSCU, 0x4, -1), # ALT_MPUSCU
    (ALT_MPUL2, 0x4, -1), # ALT_MPUL2
    (ALT_OCRAM, 0x10000, -1), # ALT_OCRAM
]

def __get_va__(pa):
    for idx in range(len(__ranges__)):
        (pa_begin, pa_nbytes, va_begin) = __ranges__[idx]
        
        # if pa falls inside [pa_begin, pa_begin + pa_nbytes)
        if pa >= pa_begin and pa - pa_begin < pa_nbytes:
            # print("Physical address is in [0x%X, 0x%X)" % (pa_begin, pa + pa_nbytes))
            
            # if not mapped yet
            if va_begin == -1:
                va_begin = __de0mem_c__.mmap(pa_begin, pa_nbytes)
                __ranges__[idx] = (pa_begin, pa_nbytes, va_begin)
            
            return va_begin + (pa - pa_begin)
            
    raise RuntimeError("Physical address 0x%X is invalid" % pa)
    
# write
def write_int8_to_pa(pa, val):
    va = __get_va__(pa)
    __de0mem_c__.write_int8_to_va(va, val)

def write_int16_to_pa(pa, val):
    va = __get_va__(pa)
    __de0mem_c__.write_int16_to_va(va, val)

def write_int32_to_pa(pa, val):
    va = __get_va__(pa)
    __de0mem_c__.write_int32_to_va(va, val)
    
def write_uint8_to_pa(pa, val):
    va = __get_va__(pa)
    __de0mem_c__.write_uint8_to_va(va, val)
    
def write_uint16_to_pa(pa, val):
    va = __get_va__(pa)
    __de0mem_c__.write_uint16_to_va(va, val)
    
def write_uint32_to_pa(pa, val):
    va = __get_va__(pa)
    __de0mem_c__.write_uint32_to_va(va, val)
    
# read
def read_int8_from_pa(pa):
    va = __get_va__(pa)
    return __de0mem_c__.read_int8_from_va(va)
    
def read_uint8_from_pa(pa):
    va = __get_va__(pa)
    return __de0mem_c__.read_uint8_from_va(va)
    
def read_int16_from_pa(pa):
    va = __get_va__(pa)
    return __de0mem_c__.read_int16_from_va(va)
    
def read_uint16_from_pa(pa):
    va = __get_va__(pa)
    return __de0mem_c__.read_uint16_from_va(va)
    
def read_int32_from_pa(pa):
    va = __get_va__(pa)
    return __de0mem_c__.read_int32_from_va(va)
    
def read_uint32_from_pa(pa):
    va = __get_va__(pa)
    return __de0mem_c__.read_uint32_from_va(va)
    