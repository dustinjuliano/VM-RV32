# Tutorial 57: Advanced Expressions
# Nested logic and complex state.

# sp initialized to 65536
li a1, 20
li a2, 30

# Using and/or/not to verify complex invariants.
@assert and(lt(a0, a1), lt(a1, a2))
@assert or(eq(a0, 0), gt(a0, 5))
@assert not(eq(a0, a1))

# sp initialized to 65536
@assert and(eq(sp, 65536), eq(zero, 0))
