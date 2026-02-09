# Tutorial 03: Numeric Literals
# Understanding Decimal, Hexadecimal, and Binary formats.

# 1. Decimal (Base 10)
# The standard format we use effectively everywhere.
addi x1, x0, 42
@assert eq(x1, 42)

# 2. Hexadecimal (Base 16)
# Prefixed with 0x. Useful for bitmasks and addresses.
# 0x2A = 2*16 + 10 = 42
addi x2, x0, 0x2A
@assert eq(x2, 42)
@assert eq(x1, x2)

# 3. Binary (Base 2)
# Prefixed with 0b. Useful for visualizing individual bits.
# 0b101010 = 32 + 8 + 2 = 42
addi x3, x0, 0b101010
@assert eq(x3, 42)
@assert eq(x3, x1)

# 4. Negative Numbers
# Represented in Two's Complement.
addi x4, x0, -1
@assert eq(x4, 0xFFFFFFFF)
@print x4
