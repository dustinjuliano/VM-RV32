# Tutorial 44: Nested Function Calls
# Why saving RA is critical.

# sp initialized to 65536
jal ra, .outer
jal x0, .done

.outer:
  addi sp, sp, -16
  sw ra, 12(sp) # Save OUTER's return address
  
  jal ra, .inner # This overwrites ra!

  lw ra, 12(sp) # Restore OUTER's return address
  addi sp, sp, 16
  jalr x0, ra, 0

.inner:
  # Leaf function (no calls), doesn't need to save ra to stack
  jalr x0, ra, 0

.done:
@assert eq(sp, 65536)
