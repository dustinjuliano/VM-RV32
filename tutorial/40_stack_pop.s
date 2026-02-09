# Tutorial 40: Popping from the Stack
# Learn to restore registers and deallocate.

# Setup: Stack has 42 at top
# Setup: Stack has 42 at top
# sp initialized to 65536
addi sp, sp, -4
addi x1, x0, 42
sw x1, 0(sp)

# To 'pop' into x2:
# 1. Load the value
# 2. Deallocate (sp = sp + 4)
lw t0, 0(sp)
addi sp, sp, 4

@assert eq(t0, 42)
@assert eq(sp, 65536)
@print sp
