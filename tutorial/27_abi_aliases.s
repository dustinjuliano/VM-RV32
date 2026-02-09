# Tutorial 27: Register Aliases
# Learn the standard architectural names vs ABI names.

# RISC-V registers have two names: their hardware index and their ABI role.
# Hardware: x0, x1, x2, ...
# ABI: zero, ra, sp, gp, tp, t0-t6, s0-s11, a0-a7

addi zero, zero, 100 # x0 is hardwired to 0. Writing to 'zero' does nothing.
@assert eq(zero, 0)

addi x1, x0, 42
# x1 is also known as 'ra' (Return Address).
@assert eq(ra, 42)

# sp is initialized to 0x10000 by CPU
