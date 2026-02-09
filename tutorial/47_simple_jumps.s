# Tutorial 47: J and JR
# The simplest jump forms.

# 1. J label (Jump)
# Pseudo for: jal x0, label
j .next
addi a0, x0, 1 # Skipped
.next:
@assert eq(a0, 0)

# 2. JR rs (Jump Register)
# Pseudo for: jalr x0, rs, 0
la t0, .target
jr t0
addi a0, x0, 1 # Skipped
.target:
@assert eq(a0, 0)
