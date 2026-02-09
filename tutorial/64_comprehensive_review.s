# Tutorial 64: Comprehensive Architecture Review
# Bringing it all together.

# 1. ABI Check
# sp initialized to 65536
li a0, 5
li a1, 10

# 2. Logic & Arithmetic
add s0, a0, a1 # s0 = 15
xor t0, s0, a0 # t0 = 15 ^ 5 = 10

# 3. Memory & Stack
addi sp, sp, -4
sw s0, 0(sp)
@assert eq(m[65532, u32], 15)

# 4. Control Flow
mv a0, s0
call .done
j .real_done

.done:
  ret

.real_done:
addi sp, sp, 4
@assert eq(a0, 15)
@assert eq(sp, 65536)
