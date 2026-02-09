# Tutorial 52: Zero-Relative Branches
# BEQZ, BNEZ, BGTZ, BLTZ, BGEZ, BLEZ

li a0, 10
li a1, 0

# 1. BNEZ (Branch if Not Equal to Zero)
bnez a0, .not_zero
@assert eq(x0, 1) # Error
.not_zero:

# 2. BEQZ (Branch if Equal to Zero)
beqz a1, .is_zero
@assert eq(x0, 1) # Error
.is_zero:

@assert eq(a0, 10)
