# Tutorial 06: R-Type Deep Dive - Arithmetic
# Learn about ADD and SUB (Register-Register)

# 1. Setup registers
addi x1, x0, 10
addi x2, x0, 5

# 2. ADD: rd = rs1 + rs2
add x3, x1, x2
@assert eq(x3, 15)

# 3. SUB: rd = rs1 - rs2
sub x4, x1, x2
@assert eq(x4, 5)

# 4. SUB with negative results (Two's Complement)
sub x5, x2, x1
@assert eq(x5, 0xFFFFFFFB) # -5
@print x5
