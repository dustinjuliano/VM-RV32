# Tutorial 10: I-Type Mechanics - Arithmetic
# Learn about ADDI, SLTI, and SLTIU

addi x1, x0, 10

# 1. ADDI (Add Immediate): x2 = x1 + (-5)
addi x2, x1, -5
@assert eq(x2, 5)

# 2. SLTI (Set Less Than Immediate): x3 = (x1 < 20) ? 1 : 0
slti x3, x1, 20
@assert eq(x3, 1)

# 3. SLTIU (Set Less Than Immediate Unsigned): x4 = (x1 < -1) ? 1 : 0
# -1 is sign-extended to 0xFFFFFFFF, which is the largest unsigned word.
sltiu x4, x1, -1
@assert eq(x4, 1)
