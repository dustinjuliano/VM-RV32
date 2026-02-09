# Tutorial 56: Advanced @print Usage
# Learn labels and varied register formats.

li a0, 0xABC
# Standard register print
@print a0

# You can also print the PC or x0
@print PC
@print x0

# Printing can help track register changes across many lines
addi a0, a0, 1
@print a0
addi a0, a0, 1
@print a0
