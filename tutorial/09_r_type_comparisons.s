# Tutorial 09: R-Type Deep Dive - Comparisons
# Learn about SLT and SLTU

addi x1, x0, -1 # 0xFFFFFFFF
addi x2, x0, 1

# 1. SLT (Set Less Than - Signed):
# -1 < 1 is true (1)
slt x3, x1, x2
@assert eq(x3, 1)

# 2. SLTU (Set Less Than - Unsigned):
# 0xFFFFFFFF < 1 is false (0)
sltu x4, x1, x2
@assert eq(x4, 0)
