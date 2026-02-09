# Tutorial 58: Memory in Assertions
# Verifying data structures indirectly.

li t0, 0 # Address
li t1, 0xDE
sb t1, 0(t0)
li t1, 0xAD
sb t1, 1(t0)

# Check bytes individually
@assert eq(m[0, u8], 0xDE)
@assert eq(m[1, u8], 0xAD)

# Check as a half-word (Little Endian: 0xADDE)
@assert eq(m[0, u16], 0xADDE)
