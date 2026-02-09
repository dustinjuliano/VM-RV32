# Tutorial 01: The Meta-Syntax Engine
# Before learning instructions, learn how to audit the machine.

# addi (Add Immediate): x1 = x0 + 100
addi x1, x0, 100

# @print: Displays the value of a register during execution.
@print x1

# @assert: Halts if the condition is false.
# eq(a, b) checks if a equals b.
@assert eq(x1, 100)

addi x1, x1, 50
@print x1
@assert eq(x1, 150)
