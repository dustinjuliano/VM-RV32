# Tutorial 02: Register Expressions
# Learn to compare registers and use constants.

addi x1, x0, 10
addi x2, x0, 20

# We can use register names in assertions.
@assert lt(x1, x2)
@assert gt(x2, x1)
@assert ne(x1, x2)

# Expressions can have nested logic.
# and(cond1, cond2)
@assert and(eq(x1, 10), eq(x2, 20))
