# Tutorial 12: I-Type Mechanics - Shift Immediates
# Learn about SLLI, SRLI, and SRAI

addi x1, x0, 2

# 1. SLLI (Shift Left Logical Immediate): x2 = 2 << 4
slli x2, x1, 4
@assert eq(x2, 32)

addi x3, x0, -1 # 0xFFFFFFFF

# 2. SRLI (Shift Right Logical Immediate): Logic 0-fill
srli x4, x3, 4
@assert eq(x4, 0x0FFFFFFF)

# 3. SRAI (Shift Right Arithmetic Immediate): Sign-fill
srai x5, x3, 4
@assert eq(x5, 0xFFFFFFFF)
