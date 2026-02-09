# Tutorial 21: JALR - Jump and Link Register
# Learn indirect jumps.

# JALR rd, rs1, offset
# 1. rd = PC + 4
# 2. PC = rs1 + offset (and LSB set to 0)

li x1, 12 # Address of .target_jump (4 + 4 + 4)
# Address 0: li (pseudo -> addi x1, x0, 12) [4 bytes]
# Address 4: jalr (4 bytes) -> jumps to 12
jalr x2, x1, 0
addi x3, x0, 1 # Skipped [Address 8]
.target_jump: # [Address 12]
@assert eq(x2, 8) # JALR was at PC=4, so RA is 8
@print x2
