# Tutorial 48: CALL and RET
# The standard function abstractions.

# 1. CALL label
# Pseudo for: auipc ra, offset_hi; jalr ra, ra, offset_lo
# (Simplified: it calls a function and saves RA)

call .test_func
@assert eq(a0, 1)
j .done

.test_func:
  addi a0, x0, 1
  # 2. RET (Return)
  # Pseudo for: jalr x0, ra, 0
  ret

.done:
@print a0
