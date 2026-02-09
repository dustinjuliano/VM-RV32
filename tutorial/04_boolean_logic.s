# Tutorial 04: Advanced Assertions
# Using boolean logic for complex state verification.

addi x1, x0, 100
addi x2, x0, 200

# or(cond1, cond2)
# not(cond)
@assert or(eq(x1, 100), eq(x1, 0))
@assert not(eq(x2, x1))

# Complex nested logic
@assert and(gt(x2, x1), not(lt(x2, 100)))
@print x2
