# Tutorial 38: Frame Pointer (fp)
# Deep dive into x8/s0 role.

# While x8 is a saved register, it is commonly used as a 'Frame Pointer'.
# It points to the base of the current stack frame.

li fp, 2048
@assert eq(s0, 2048)
@assert eq(x8, 2048)
@print fp
