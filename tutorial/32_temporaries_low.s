# Tutorial 32: Temporary Registers (t0-t2)
# Roles of x5, x6, x7.

# Temporaries are registers that are NOT preserved across function calls.
# If you call a function, it might overwrite these.

addi t0, x0, 1
addi t1, x0, 2
addi t2, x0, 3

@assert eq(x5, 1)
@assert eq(x6, 2)
@assert eq(x7, 3)
