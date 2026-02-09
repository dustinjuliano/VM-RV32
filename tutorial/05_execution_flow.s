# Tutorial 05: The Execution Loop
# Understanding how the emulator steps through code.

addi x1, x0, 1
addi x2, x0, 2
addi x3, x0, 3

# Execution proceeds line by line.
@assert eq(x1, 1)
@assert eq(x2, 2)
@assert eq(x3, 3)

# If no more instructions are found, the emulator finishes.
# PC (Program Counter) starts at 0 and increments by 4 typically.
@print x0
@print x1
