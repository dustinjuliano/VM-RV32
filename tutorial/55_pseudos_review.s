# Tutorial 55: Pseudos Review
# Combining shortcuts for clean code.

# Instead of:
# lui x10, 0x1000
# addi x10, x10, 0x500
# addi x11, x0, 1
# beq x10, x11, .label

# Use:
li a0, 42
li a1, 42
beq a0, a1, .match
  nop
.match:
  mv a2, a0

@assert eq(a2, 42)
