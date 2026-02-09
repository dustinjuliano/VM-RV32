# Tutorial 35: Function Arguments (a2-a7)
# Roles of x12-x17.

# These are used to pass additional arguments (3rd through 8th).

addi a2, x0, 3
addi a3, x0, 4
addi a4, x0, 5
addi a5, x0, 6
addi a6, x0, 7
addi a7, x0, 8

@assert eq(x12, 3)
@assert eq(x17, 8)
@print a7
