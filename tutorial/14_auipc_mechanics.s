# Tutorial 14: Upper Immediates - AUIPC
# Learn PC-relative addressing.

# AUIPC (Add Upper Immediate to PC): rd = PC + (imm << 12)
# If this instruction is at address 0x100:
# x1 = 0x100 + (0x10 << 12) = 0x10100

auipc x1, 0x10
@print x1

# Note: In our emulator, addresses start at 0.
# The emulator execution will show the current PC.
