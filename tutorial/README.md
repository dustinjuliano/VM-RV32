# RISC-V Emulator Tutorial Series

Welcome to the comprehensive RISC-V 32I tutorial series! This curriculum is designed to take you from zero to a solid understanding of the RISC-V architecture and its assembly language.

## How to use this tutorial
Run each file using the `rvsim` alias (or `python3 main.py`) and observe the output. Each file contains `@assert` statements that verify your understanding of the machine state.

```bash
./rvsim tutorial/01_meta_syntax_basics.s
```

## Curriculum Overview

### Phase 1: Basic Mechanics (01-16)
- **01-05**: Emulator meta-syntax, expressions, and memory inspection.
- **06-09**: R-type instructions (Arithmetic, Logic, Shifts, Comparisons).
- **10-12**: I-type instructions (Arithmetic, Logic, Shifts with Immediates).
- **13-14**: Upper Immediates (LUI, AUIPC).
- **15-16**: Memory Loads and Stores.

### Phase 2: Control Flow (17-26)
- **17-19**: Conditional Branches (BEQ, BNE, BLT, BGE, BLTU, BGEU).
- **20-21**: Jumps (JAL, JALR).
- **22-26**: PC-relative offsets, loops, and control flow review.

### Phase 3: The ABI (27-38)
- **27-28**: Register aliases and the special role of 'zero'.
- **29-31**: RA, SP, GP, and TP registers.
- **32-37**: Argument (a), Saved (s), and Temporary (t) registers.
- **38**: The Frame Pointer (fp).

### Phase 4: Stack & Frames (39-45)
- **39-41**: Stack push, pop, and multi-word operations.
- **42-43**: Function Prologues and Epilogues.
- **44-45**: Nested calls and Leaf functions.

### Phase 5: Pseudo-instructions (46-55)
- **46-48**: LI, LA, J, CALL, and RET.
- **49-51**: MV, NEG, NOT, and NOP.
- **52-55**: Branch and Comparison shortcuts.

### Phase 6: Advanced Verification (56-64)
- **56-59**: Advanced emulator meta-syntax and memory expressions.
- **60-63**: Label math, alignment, and instruction formats.
- **64**: Comprehensive architectural review.
