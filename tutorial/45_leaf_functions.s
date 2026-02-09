# Tutorial 45: Leaf Functions vs Non-leaf Functions
# Efficiency optimizations.

# A 'leaf' function does not call any other functions.
# It does NOT need to save RA to the stack, saving memory and time.

# sp initialized to 65536
jal ra, .leaf
jal x0, .done

.leaf:
  # No prologue/epilogue needed if no s-regs or calls.
  addi a0, a0, 1
  jalr x0, ra, 0

.done:
@assert eq(a0, 1)
