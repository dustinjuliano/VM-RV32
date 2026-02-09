# Tutorial 46: LI and LA
# Learn how we load values and labels easily.

# 1. LI (Load Immediate): li rd, imm
# This is a pseudo for ADDI (if small) or LUI + ADDI (if large).
li a0, 42
@assert eq(a0, 42)

li a1, 0x12345678
@assert eq(a1, 0x12345678)

# 2. LA (Load Address): la rd, label
# This is a pseudo for AUIPC + ADDI.
la a2, .my_label
.my_label:
@print a2
