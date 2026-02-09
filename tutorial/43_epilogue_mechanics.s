# Tutorial 43: The Epilogue
# Standards for exiting a function.

# 1. Restore saved registers
# 2. Restore RA
# 3. Deallocate stack frame
# 4. Return via jalr x0, ra, 0

jal ra, .my_func
jal x0, .done

.my_func:
  # Prologue
  addi sp, sp, -16
  sw ra, 12(sp)
  sw s0, 8(sp)

  # Body
  addi s0, x0, 99

  # Epilogue
  lw s0, 8(sp)
  lw ra, 12(sp)
  addi sp, sp, 16
  jalr x0, ra, 0

.done:
@assert eq(sp, 65536)
@print sp
