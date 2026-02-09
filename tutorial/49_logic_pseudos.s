# Tutorial 49: MV, NEG, NOT
# Quick logic shortcuts.

addi a1, x0, 10

# 1. MV (Move): mv rd, rs
# Pseudo for: addi rd, rs, 0
mv a2, a1
@assert eq(a2, 10)

# 2. NEG (Negate): neg rd, rs
# Pseudo for: sub rd, x0, rs
neg a3, a1
@assert eq(a3, -10)

# 3. NOT (Invert): not rd, rs
# Pseudo for: xori rd, rs, -1
li a4, 0x0
not a5, a4
@assert eq(a5, 0xFFFFFFFF)
