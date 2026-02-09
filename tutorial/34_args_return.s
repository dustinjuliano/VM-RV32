# Tutorial 34: Arguments & Return Values (a0-a1)
# Roles of x10, x11.

# a0-a1 are used for both passing the first two arguments
# AND for returning values from a function.

addi a0, x0, 10
addi a1, x0, 20

@assert eq(x10, 10)
@assert eq(x11, 20)
