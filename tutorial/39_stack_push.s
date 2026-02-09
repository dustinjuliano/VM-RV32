# Tutorial 39: Pushing to the Stack
# Learn the basic stack allocation and store pattern.

# Initialize SP
# sp initialized to 65536

# To 'push' x1 (42):
# 1. Allocate space (sp = sp - 4)
# 2. Store the value
addi x1, x0, 42
addi sp, sp, -4
sw x1, 0(sp)

@assert eq(sp, 65532)
@assert eq(m[65532, u32], 42)
@print sp
@print_mem 1020 u32 1
