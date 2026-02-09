# Tutorial 37: More Saved Registers (s2-s11)
# Roles of x18-x27.

addi s2, x0, 2
addi s11, x0, 11

@assert eq(x18, 2)
@assert eq(x27, 11)
@print s11
