# Tutorial 23: Infinite Loops
# Learning the 'J' pattern (pseudo for JAL x0, offset)

addi x1, x0, 0

.loop:
  addi x1, x1, 1
  beq x1, x0, .loop # Never taken

# In real assembly, we use J label
# jal x0, .loop
jal x0, .end_loop
  addi x1, x1, 100 # Dead code
.end_loop:

@assert eq(x1, 1)
