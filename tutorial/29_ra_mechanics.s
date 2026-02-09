# Tutorial 29: Return Address (ra)
# Understanding x1's special role in JAL.

# JAL ra, offset saves PC+4 into ra.
jal ra, .next
.next:
# If JAL was at PC=0, ra should be 4.
@print ra
@assert eq(ra, 4)

# We use ra to return from functions later (using jalr).
@assert eq(x1, ra)
