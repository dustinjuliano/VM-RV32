# Tutorial 53: Other Branch Pseudos
# BGT, BLE, BGTU, BLEU

li a0, 20
li a1, 10

# 1. BGT (Branch if Greater Than): Pseudo for BLT with swapped rs1, rs2
bgt a0, a1, .ok
@assert eq(x0, 1)
.ok:

# 2. BLE (Branch if Less or Equal): Pseudo for BGE with swapped rs1, rs2
ble a1, a0, .ok2
@assert eq(x0, 1)
.ok2:

@print a0
