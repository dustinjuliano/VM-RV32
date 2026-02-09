# Tutorial 31: Global (gp) and Thread (tp) Pointers
# Roles of x3 and x4.

# x3 (gp) is used to point to the middle of the global data section.
# x4 (tp) is used for thread-local storage.
# In simple programs, these are rarely changed by the user.

li gp, 2048
@assert eq(x3, 2048)

li tp, 4096
@assert eq(x4, 4096)
