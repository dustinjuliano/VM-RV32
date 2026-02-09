# Tutorial 07: R-Type Deep Dive - Logical
# Learn about AND, OR, and XOR

addi x1, x0, 0b1100
addi x2, x0, 0b1010

# 1. AND: bitwise intersection
and x3, x1, x2
@assert eq(x3, 0b1000)

# 2. OR: bitwise union
or x4, x1, x2
@assert eq(x4, 0b1110)

# 3. XOR: bitwise difference
xor x5, x1, x2
@assert eq(x5, 0b0110)
