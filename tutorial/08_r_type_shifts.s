# Tutorial 08: R-Type Deep Dive - Shifts
# Learn about SLL, SRL, and SRA

addi x1, x0, 0b0001
addi x2, x0, 2

# 1. SLL (Shift Left Logical): x3 = x1 << 2
sll x3, x1, x2
@assert eq(x3, 0b0100)

# 2. SRL (Shift Right Logical): x4 = 0x80000000 >> 1
# This logic fills with 0s.
addi x4, x0, 1
slli x4, x4, 31 # x4 = 0x80000000
addi x5, x0, 1
srl x6, x4, x5
@assert eq(x6, 0x40000000)

# 3. SRA (Shift Right Arithmetic): Sign-preserving shift
# This logic fills with the sign bit.
sra x7, x4, x5
@assert eq(x7, 0xC0000000)
