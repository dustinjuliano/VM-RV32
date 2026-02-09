# Tutorial 28: The Zero Register
# Deep dive into 'zero' (x0).

# The 'zero' register ALWAYS contains 0. It cannot be overwritten.
addi zero, zero, 50
@assert eq(zero, 0)

# It is used for clearing registers:
addi x1, x0, 100
add x1, x0, x0  # x1 = 0 + 0
@assert eq(x1, 0)

# Or for NOPs:
add zero, zero, zero
@print zero
