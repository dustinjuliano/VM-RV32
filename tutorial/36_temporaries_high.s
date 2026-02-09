# Tutorial 36: More Temporaries (t3-t6)
# Roles of x28-x31.

addi t3, x0, 30
addi t4, x0, 40
addi t5, x0, 50
addi t6, x0, 60

@assert eq(x28, 30)
@assert eq(x31, 60)
