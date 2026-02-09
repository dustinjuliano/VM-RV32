# Tutorial 25: Large Forward Jumps
# Using JAL to cross larger distances.

addi x1, x0, 10
jal x0, .far_away

# ... Imagine many instructions here ...
addi x1, x0, 20 # Skipped

.far_away:
@assert eq(x1, 10)
