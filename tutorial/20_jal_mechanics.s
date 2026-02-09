# Tutorial 20: JAL - Jump and Link
# Learn how to jump and save the return address.

# JAL rd, offset
# 1. rd = PC + 4 (Return Address)
# 2. PC = PC + offset

jal x1, .target
addi x2, x0, 1 # This is the "return address" target
.target:
@print x1
# In our emulator, addresses are small. x1 should be 4.
@assert eq(x1, 4)
