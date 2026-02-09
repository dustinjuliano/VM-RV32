# Tutorial 16: Memory Stores - Partial Writes
# Learn SB and SH

# Reset memory
li x2, 0x100 # Use valid address
sb x3, 0(x2)
sh x4, 0(x2)
sw x5, 0(x2)
sw x0, 0(x0)

addi x1, x0, 0x12
# 1. SB (Store Byte): Only Mem[0] changes
sb x1, 0(x0)
@assert eq(m[0, u32], 0x12)

li x2, 0x3456
# 2. SH (Store Half): Mem[0:1] changes
sh x2, 0(x0)
@assert eq(m[0, u32], 0x3456)

# Byte 0 is 0x56, Byte 1 is 0x34
@assert eq(m[0, u8], 0x56)
@assert eq(m[1, u8], 0x34)
