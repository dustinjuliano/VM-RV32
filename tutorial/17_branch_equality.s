# Tutorial 17: Branching - Equality
# Learn BEQ and BNE

addi x1, x0, 10
addi x2, x0, 10
addi x3, x0, 20

# 1. BEQ (Branch if Equal): rs1 == rs2
beq x1, x2, .matched
addi x4, x0, 1  # This should be skipped
.matched:
@assert eq(x4, 0)

# 2. BNE (Branch if Not Equal): rs1 != rs2
bne x1, x3, .diff
addi x5, x0, 1 # This should be skipped
.diff:
@assert eq(x1, 10)
@print x1
