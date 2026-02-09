# Tutorial 22: PC-Relative Addressing
# How branches and jumps use offsets.

# Branches and JAL use signed offsets relative to current PC.
# This allows code to be "Position Independent".

addi x1, x0, 0
beq x0, x0, +8  # Skip next instruction
addi x1, x0, 1
addi x2, x0, 2

@assert eq(x1, 0)
@assert eq(x2, 2)
