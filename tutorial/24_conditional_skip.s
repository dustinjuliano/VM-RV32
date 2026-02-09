# Tutorial 24: Conditional Skip Pattern
# Common assembly pattern: skip if not equal

addi x1, x0, 5
addi x2, x0, 10

# if (x1 == 5) x2 = 20;
addi x3, x0, 5
bne x1, x3, .skip
  addi x2, x0, 20
.skip:

@assert eq(x2, 20)
