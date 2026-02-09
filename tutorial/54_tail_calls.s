# Tutorial 54: Tail Calls
# Tail call optimization concept.

# A 'tail call' is when a function's last action is calling another function.
# Instead of 'call' then 'ret', we can just 'j'.
# This avoids an extra stack push/pop or RA change.

call .func_a
j .done

.func_a:
  addi a0, x0, 1
  j .func_b # Tail call!

.func_b:
  addi a0, a0, 1
  ret # Returns directly to the original caller of func_a

.done:
@assert eq(a0, 2)
