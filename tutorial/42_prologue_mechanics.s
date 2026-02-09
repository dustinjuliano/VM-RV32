# Tutorial 42: The Prologue
# Standards for entering a function.

# 1. Allocate stack frame (must be 16-byte aligned in many ABIs)
# 2. Save RA (Return Address)
# 3. Save any preserved (s) registers used in the function

# sp initialized to 65536
jal ra, .my_func
jal x0, .done

.my_func:
  # Prologue
  addi sp, sp, -16
  sw ra, 12(sp)
  sw s0, 8(sp)

  # ... function body ...
  addi s0, x0, 42
  @assert eq(s0, 42)

  # (Return is covered in 43)
  jalr x0, ra, 0

.done:
@assert eq(ra, 4)
