# Tutorial 61: Data Section Alignment
# Concept of word boundaries.

# RISC-V 32I expects loads/stores to be naturally aligned.
# Word (4 bytes) at 0, 4, 8...
# Half (2 bytes) at 0, 2, 4...

li t0, 1 # Unaligned word address
li t1, 42
# sw t0, t1, 0 # This might cause an Exception/Fault on real hardware!

# Our emulator allows it, but students should learn to align:
li t0, 0
sw t1, 0(t0) # Good
sw t1, 4(t0) # Good
