# Tutorial 62: Byte Ordering
# Understanding Little Endian.

li t0, 0
li t1, 0x12345678
sw t1, 0(t0)

# Byte 0 is the LEAST significant byte
@assert eq(m[0, u8], 0x78)
@assert eq(m[1, u8], 0x56)
@assert eq(m[2, u8], 0x34)
@assert eq(m[3, u8], 0x12)

@print_mem 0 u8 4
