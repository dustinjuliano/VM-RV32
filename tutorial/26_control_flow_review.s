# Tutorial 26: Control Flow Review
# Combining branches and jumps.

addi x1, x0, 0
addi x2, x0, 3

.loop:
  beq x1, x2, .exit
  addi x1, x1, 1
  jal x0, .loop
.exit:

@assert eq(x1, 3)
@print x1
