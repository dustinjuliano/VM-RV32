# Tutorial 13: Upper Immediates - LUI
# Learn how to load large constants.

# LUI (Load Upper Immediate): rd = imm << 12
# Used to set the top 20 bits of a register.
lui x1, 0x12345

# x1 = 0x12345000
@assert eq(x1, 0x12345000)
@print x1

# Combine with ADDI to set all 32 bits:
# x1 = 0x12345678
addi x1, x1, 0x678
@assert eq(x1, 0x12345678)
