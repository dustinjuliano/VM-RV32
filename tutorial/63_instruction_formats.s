# Tutorial 63: Instruction Formats
# Overview of R, I, S, B, U, J

# Every instruction we've used follows one of these formats.
# They all occupy exactly 4 bytes (32 bits).

add x5, x6, x7   # R-type
addi x5, x6, 10  # I-type
sw x5, 0(x6)      # S-type
beq x5, x6, .label # B-type
lui x5, 0x1       # U-type
jal x5, .label    # J-type

# The consistency of these formats is what makes RISC-V elegant.
.label:
  nop
