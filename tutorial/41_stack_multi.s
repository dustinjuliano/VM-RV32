# Tutorial 41: Multi-word Stack Operations
# Allocating space for multiple registers at once.

# sp initialized to 65536

# Allocate 12 bytes for 3 registers
addi sp, sp, -12
sw s0, 8(sp)
sw s1, 4(sp)
sw s2, 0(sp)

# ... do work ...

# Restore
lw s0, 8(sp)
lw s1, 4(sp)
lw s2, 0(sp)
addi sp, sp, 12

@assert eq(sp, 65536)
