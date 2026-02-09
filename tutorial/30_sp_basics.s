# Tutorial 30: Stack Pointer (sp)
# Intro to x2's role.

# By convention, sp points to the top of the stack.
# The stack grows DOWN (to lower addresses).

# sp initialized to 65536 by default
@assert eq(sp, 65536)

# Growing the stack by 16 bytes:
addi sp, sp, -16
@assert eq(sp, 65520)

# Shrinking the stack (cleaning up):
addi sp, sp, 16
@assert eq(sp, 65536)
