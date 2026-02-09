# Tutorial 19: Branching - Unsigned Comparisons
# Learn BLTU and BGEU

addi x1, x0, -1 # 0xFFFFFFFF
addi x2, x0, 1

# 1. BLTU (Branch if Less Than Unsigned): 0xFFFFFFFF < 1 is False
bltu x1, x2, .oops
addi x3, x0, 1
.oops:
@assert eq(x3, 1)

# 2. BGEU (Branch if Greater or Equal Unsigned): 0xFFFFFFFF >= 1 is True
bgeu x1, x2, .is_larger
addi x4, x0, 1 # Skipped
.is_larger:
@assert eq(x4, 0)
