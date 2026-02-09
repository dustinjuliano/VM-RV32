# Tutorial 15: Memory Loads - Signed vs Unsigned
# Learn LB, LH vs LBU, LHU

# Store a pattern: 0x000080FF
# Byte 0: 0xFF, Byte 1: 0x80
li x1, 0x80FF
sw x1, 0(x0)

# 1. LB (Load Byte - Signed): FF -> -1
lb x2, 0(x0)
@assert eq(x2, 0xFFFFFFFF)

# 2. LBU (Load Byte Unsigned): FF -> 255
lbu x3, 0(x0)
@assert eq(x3, 0xFF)

# 3. LH (Load Half - Signed): 80FF -> -32513
lh x4, 0(x0)
@assert eq(x4, 0xFFFF80FF)

# 4. LHU (Load Half Unsigned): 80FF -> 33023
lhu x5, 0(x0)
@assert eq(x5, 0x80FF)
