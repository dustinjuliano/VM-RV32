# Tutorial 56: Advanced @print Usage
# Learn labels, varied register formats, and expressions.

li a0, 0xABC
# Standard register print
@print a0

# You can also print the PC or x0
@print PC
@print x0

# Printing can help track register changes
addi a0, a0, 1
@print a0

# NEW: Arithmetic expressions in @print
# You can perform calculations directly in the print statement
@print add(a0, 10)
@print sub(a0, 0xABC)

# NEW: Memory inspection with calculated addresses
li sp, 0x1000
li t0, 0xDEADBEEF
sw t0, 4(sp)

# Print memory at sp+4
@print m[add(sp, 4), u32]

# Complex nesting is allowed
li t1, 5
li t2, 2
@print mul(add(t1, t2), sub(t1, t2))
