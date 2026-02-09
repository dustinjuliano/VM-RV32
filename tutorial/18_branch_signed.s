# Tutorial 18: Branching - Signed Comparisons
# Learn BLT and BGE

addi x1, x0, -10
addi x2, x0, 5

# 1. BLT (Branch if Less Than - Signed): -10 < 5 is True
blt x1, x2, .is_less
addi x3, x0, 1 # Skipped
.is_less:
@assert eq(x3, 0)

# 2. BGE (Branch if Greater or Equal - Signed): 5 >= -10 is True
bge x2, x1, .is_ge
addi x4, x0, 1 # Skipped
.is_ge:
@assert eq(x4, 0)
