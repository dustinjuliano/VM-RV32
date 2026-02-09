# Tutorial 33: Saved Registers (s0-s1)
# Roles of x8, x9.

# Saved registers MUST be preserved across function calls.
# If a function wants to use them, it must save them to the stack first
# and restore them before returning.

addi s0, x0, 123
addi s1, x0, 456

@assert eq(x8, 123)
@assert eq(x9, 456)

# x8 is also known as 'fp' (Frame Pointer).
@assert eq(fp, 123)
@print s1
