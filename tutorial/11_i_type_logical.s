# Tutorial 11: I-Type Mechanics - Logical
# Learn about ANDI, ORI, and XORI

addi x1, x0, 0b1010

# 1. ANDI: bitwise intersection with constant
andi x2, x1, 0b1100
@assert eq(x2, 0b1000)

# 2. ORI: bitwise union with constant
ori x3, x1, 0b0101
@assert eq(x3, 0b1111)

# 3. XORI: bitwise flip with constant
xori x4, x1, 0b1111
@assert eq(x4, 0b0101)
@print x4
