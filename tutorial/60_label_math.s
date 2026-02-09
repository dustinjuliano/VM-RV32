# Tutorial 60: Label Math
# Relative offsets and labels as constants.

# Labels are just addresses.
la a0, .target
la a1, .loop
# You can subtract labels to get distances!
# (Note: In this assembler, labels are absolute, but we can verify distances)
# @assert eq(sub(label1, label2), distance)

.loop:
  nop
.target:
@print a0
@print a1
