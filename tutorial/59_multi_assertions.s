# Tutorial 59: Multi-line Assertions
# Organizing verification logic.

li a0, 10
li a1, 11

@assert eq(a0, 10)
@assert eq(a1, 11)
# You can have many assertions in a row to check a whole "state block"
@assert lt(a0, a1)
@assert ne(a0, a1)
