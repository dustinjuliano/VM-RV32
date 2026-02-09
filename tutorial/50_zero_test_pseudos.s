# Tutorial 50: Zero-testing Shortcuts
# SEQZ, SNEZ, SLTZ, SGTZ

li a0, 0
li a1, 42

# 1. SEQZ (Set if Equal to Zero): rd = (rs == 0)
seqz a2, a0
@assert eq(a2, 1)

# 2. SNEZ (Set if Not Equal to Zero): rd = (rs != 0)
snez a3, a1
@assert eq(a3, 1)

# 3. SLTZ (Set if Less Than Zero): rd = (rs < 0)
li a4, -1
sltz a5, a4
@assert eq(a5, 1)
