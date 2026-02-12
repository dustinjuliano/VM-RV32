# VM-RV32: RISC-V 32I Assembly Emulator

An educational tool for learning RISC-V assembly programming. This project provides a minimalist environment for understanding the RV32I Instruction Set Architecture (ISA) and the RISC-V Calling Convention. It includes 64 tutorials (table of contents below).

## Purpose

The primary goal of this emulator is to bridge the gap between high-level architectural concepts and low-level machine execution. It includes a custom meta-syntax that allows learners to:
- **Inspect** machine state using `@print`.
- **Verify** logic using `@assert` with a powerful expression language.
- **Deep Dive** into memory with `@print_mem`.

## Getting Started

### Prerequisites

- Python 3.8 or higher.

### Installation

No installation is required. You can use the provided aliases for easier access:

**macOS/Linux:**
```bash
chmod +x rvsim
./rvsim tutorial/01_basic_debugging.s
```

**Windows:**
```cmd
rvsim.bat tutorial\01_basic_debugging.s
```

## Usage

Run the emulator by passing a RISC-V assembly file as an argument:

```bash
python3 main.py <file.s>
```

The emulator will execute the instructions and process any meta-syntax commands found in the source code.

## ISA Conformance

**VM-RV32 is fully compliant with the RISC-V User-Level ISA V2.2.**

It implements the complete **RV32I Base Integer Instruction Set**, ensuring that any valid, non-privileged RV32I program will execute correctly. This includes:
- **Integer Computational Instructions**: Arithmetic, logical, and shift operations.
- **Control Transfer Instructions**: Unconditional jumps and conditional branches.
- **Load and Store Instructions**: Byte, halfword, and word access.
- **Memory Ordering**: `FENCE` is parsed as a NOP (valid for sequential consistency models).
- **Environment Call**: `ECALL` and `EBREAK` are supported as traps.

## Stack Protection

To aid learning and debugging, VM-RV32 includes an **Opt-In Stack Safety Mechanism**:

- **Alias-Aware**: When you use the `sp` alias (e.g., `addi sp, sp, -16`), the emulator enforces strict bounds checking. It will halt execution and report an error if specific stack overflow or underflow limits are breached.
- **Hardware-Accurate**: When you use the raw register index `x2` (e.g., `addi x2, x2, -16`), these checks are **bypassed**. This mimics real hardware behavior, where the stack pointer is just a general-purpose register.

This dual-mode approach allows beginners to catch errors early while advanced users can experiment with non-standard stack manipulations.

## Educational Tutorials

The project includes a comprehensive series of **64 tutorials** designed to guide a learner from zero knowledge to a deep understanding of the RISC-V 32I ISA. Every tutorial is functionally verified as part of our automated CI suite.

### Curriculum Overview

1.  **[Basic Mechanics](tutorial/01_meta_syntax_basics.s)**: Learn the fundamental meta-syntax and assembly basics.
2.  **[Expressions](tutorial/02_expressions.s)**: Deep dive into the emulator's expression engine.
3.  **[Numeric Literals](tutorial/03_numeric_literals.s)**: Understanding decimal literals and register initialization.
4.  **[Boolean Logic](tutorial/04_boolean_logic.s)**: Basic bitwise operations (AND, OR, XOR).
5.  **[Execution Flow](tutorial/05_execution_flow.s)**: Understanding how the program counter (PC) advances.
6.  **[R-Type Arithmetic](tutorial/06_r_type_arithmetic.s)**: ADD and SUB operations.
7.  **[R-Type Logical](tutorial/07_r_type_logical.s)**: Bitwise R-type instructions.
8.  **[R-Type Shifts](tutorial/08_r_type_shifts.s)**: SLL, SRL, and SRA.
9.  **[R-Type Comparisons](tutorial/09_r_type_comparisons.s)**: SLT and SLTU mechanics.
10. **[I-Type Arithmetic](tutorial/10_i_type_arithmetic.s)**: ADDI and immediate comparisons.
11. **[I-Type Logical](tutorial/11_i_type_logical.s)**: XORI, ORI, ANDI.
12. **[I-Type Shifts](tutorial/12_i_type_shifts.s)**: SLLI, SRLI, SRAI.
13. **[LUI Mechanics](tutorial/13_lui_mechanics.s)**: Loading upper immediates for large constants.
14. **[AUIPC Mechanics](tutorial/14_auipc_mechanics.s)**: Adding upper immediate to PC.
15. **[Memory Loads](tutorial/15_memory_loads.s)**: LW, LH, LB and sign-extension.
16. **[Memory Stores](tutorial/16_memory_stores.s)**: SW, SH, SB mechanics.
17. **[Branch Equality](tutorial/17_branch_equality.s)**: BEQ and BNE operations.
18. **[Branch Signed](tutorial/18_branch_signed.s)**: BLT and BGE (signed).
19. **[Branch Unsigned](tutorial/19_branch_unsigned.s)**: BLTU and BGEU (unsigned).
20. **[JAL Mechanics](tutorial/20_jal_mechanics.s)**: Unconditional jumps and the link register.
21. **[JALR Mechanics](tutorial/21_jalr_mechanics.s)**: Indirect jumps and register-based branching.
22. **[PC-Relative Logic](tutorial/22_pc_relative.s)**: Understanding addressing in the RISC-V model.
23. **[Loops](tutorial/23_loops.s)**: Implementing basic iteration structures.
24. **[Conditional Skip](tutorial/24_conditional_skip.s)**: Using branches for logic control.
25. **[Forward Jumps](tutorial/25_forward_jumps.s)**: Managing non-linear execution.
26. **[Control Flow Review](tutorial/26_control_flow_review.s)**: Consolidating branching and jumping concepts.
27. **[ABI Aliases](tutorial/27_abi_aliases.s)**: Moving from raw registers (x) to ABI names (ra, sp).
28. **[Zero Register](tutorial/28_zero_register.s)**: The role of x0/zero in the ISA.
29. **[RA Mechanics](tutorial/29_ra_mechanics.s)**: Deep dive into the return address register.
30. **[SP Basics](tutorial/30_sp_basics.s)**: Initializing and moving the stack pointer.
31. **[GP & TP Roles](tutorial/31_gp_tp_roles.s)**: Global and Thread pointer conventions.
32. **[Temporaries (Low)](tutorial/32_temporaries_low.s)**: Using t0-t2 for scratch work.
33. **[Saved (Low)](tutorial/33_saved_low.s)**: Using s0-s1 for persistent values.
34. **[Args & Return](tutorial/34_args_return.s)**: Passing values into and out of functions (a0-a1).
35. **[More Args](tutorial/35_more_args.s)**: Using a2-a7 for complex signatures.
36. **[Temporaries (High)](tutorial/36_temporaries_high.s)**: Roles of t3-t6.
37. **[Saved (High)](tutorial/37_saved_high.s)**: Roles of s2-s11.
38. **[Frame Pointer](tutorial/38_fp_usage.s)**: Using fp/s0 for frame management.
39. **[Stack Push](tutorial/39_stack_push.s)**: Basic stack allocation and sw pattern.
40. **[Stack Pop](tutorial/40_stack_pop.s)**: Register restoration and deallocation.
41. **[Multi-word Stack](tutorial/41_stack_multi.s)**: Saving and loading multiple registers.
42. **[The Prologue](tutorial/42_prologue_mechanics.s)**: Standard function entry sequence.
43. **[The Epilogue](tutorial/43_epilogue_mechanics.s)**: Standard function exit sequence.
44. **[Nested Calls](tutorial/44_nested_calls.s)**: Managing RA and SP across call boundaries.
45. **[Leaf Functions](tutorial/45_leaf_functions.s)**: Optimized functions that make no calls.
46. **[LI & LA Pseudos](tutorial/46_li_la_pseudos.s)**: Mastering constant and address loading.
47. **[Simple Jumps](tutorial/47_simple_jumps.s)**: Using J and JR abstractions.
48. **[CALL & RET Pseudos](tutorial/48_call_ret_pseudos.s)**: Standard function call abstractions.
49. **[MV, NEG, NOT](tutorial/49_logic_pseudos.s)**: Quick logic and arithmetic aliases.
50. **[Zero-test Pseudos](tutorial/50_zero_test_pseudos.s)**: Specialized shortcuts for zero comparisons.
51. **[NOP Mechanics](tutorial/51_nop_mechanics.s)**: The role of 'no-operation' in timing and padding.
52. **[Zero Branches](tutorial/52_zero_branches.s)**: Shortcuts for comparing against zero.
53. **[Branch Pseudos](tutorial/53_branch_pseudos.s)**: BGT, BLE, BGTU, BLEU abstractions.
54. **[Tail Calls](tutorial/54_tail_calls.s)**: Optimizing final jumps in call sequences.
55. **[Pseudos Review](tutorial/55_pseudos_review.s)**: Comprehensive review of assembly abstractions.
56. **[Advanced @print & Expressions](tutorial/56_advanced_print.s)**: Learn arithmetic in debugging and complex memory inspection.
57. **[Advanced Expressions](tutorial/57_advanced_expressions.s)**: Complex bit manipulation in assertions.
58. **[Memory Expressions](tutorial/58_mem_expressions.s)**: Using m[] in verification logic.
59. **[Multi-assertions](tutorial/59_multi_assertions.s)**: Complex verification spanning multiple lines.
60. **[Label Math](tutorial/60_label_math.s)**: Performing arithmetic on symbol addresses.
61. **[Alignment Concepts](tutorial/61_alignment_concepts.s)**: Understanding word vs byte alignment in memory.
62. **[Byte Ordering](tutorial/62_endianness.s)**: Verifying Little-Endian memory layout.
63. **[Instruction Formats](tutorial/63_instruction_formats.s)**: Deep dive into R, I, S, B, U, J types.
64. **[Architecture Review](tutorial/64_comprehensive_review.s)**: Bringing it all together.

## Verification & Testing

**VM-RV32 maintains 100% functional test coverage for the entire project.**

Every component and tutorial is rigorously verified through a multi-layered testing strategy that ensures architectural accuracy and system reliability.

### Test Suite Overview

- **[Instruction Specification](tests/test_instruction_spec.py)**: Formal verification of every RV32I base instruction against its architectural state transitions.
- **[ISA Conformance](tests/test_isa_conformance.py)**: Validates the emulator against a subset of standard RISC-V test vectors.
- **[Core Logic](tests/test_core.py)**: Verifies the fundamental CPU dispatch loop, PC management, and register state consistency.
- **[Memory Model](tests/test_memory.py)**: Validates linear 32-bit addressing, overflow handling, and typed access (Word, Half, Byte).
- **[Parser & Meta-syntax](tests/test_parser.py)**: Robust validation of assembly parsing, label resolution, and expression evaluation.
- **[Assertion Engine](tests/test_meta_syntax.py)**: Ensures the `@assert` and `@print` meta-syntax commands operate correctly within the emulator environment.
- **[Stack Mechanics](tests/test_stack.py)**: Low-level verification of stack pointer manipulation and word-aligned memory access.
- **[Stack Protection](tests/test_stack_protection.py)**: Dedicated tests for our safety mechanisms, ensuring `sp` alias bounds-checking while allowing `x2` raw access.
- **[Tutorial Curriculum](tests/test_tutorials.py)**: Provides **explicit, case-by-case functional tests** for all 64 tutorials. Each tutorial is executed and its end-state verified against expected architectural results.

### Running Tests

To execute the complete test suite and verify 100% project coverage:
```bash
python3 test_runner.py
```

## Project Structure

- `main.py`: The entry point for the emulator CLI.
- `cpu.py`: The instruction execution logic.
- `memory.py`: Linear 32-bit addressable memory model.
- `registers.py`: Standard 32-register set with alias support.
- `parser.py`: Assembly and meta-syntax parser.
- `tutorial/`: The 64-part educational curriculum.
- `tests/`: Comprehensive unit and integration tests.

## AI Disclosure & Project Background

I consider this project a test of Google Antigravity and Gemini 3. That is because I designed the program and never wrote a single line of code. Not even one. I told the AI agent in Antigravity what needed to be done, corrected its design and implementation mistakes, and guided it as needed. In this way, this whole project was effectively done via a fully declarative programming approach using English. It took one evening to do something that would have taken many weeks. The alternative would have been nothing, as I do not currently have the time to work on side projects.

The purpose of this tool was to help out fellow students. We are using emulators in our course to study RISC-V, and these are simply not designed with programming in mind. Having a memory-safe local tool that can integrate into our existing editors is extremely helpful, and the tutorials also assist with learning the ISA itself. Ultimately, any assignment we would have to do goes into a designated emulator set by our instructor, which is the final word on whether or not the Assembly program will be accepted or not. This tool is a supplement, not a replacement, for that process, meant to improve productivity to allow focusing on studying.

I am impressed with Google Antigravity and the agentic programming experience. I was able to work on two other projects simultaneously while doing this one, a feat that is not humanly possible without the agentic AI. I found the process really exciting, as if the maturity of the tooling was now reaching a level where I could actually benefit from it in a tangible way. I think agentic coding tools like Antigravity have much more potential as well, and can be used for a wider range of tasks with the right setup and a little creativity. I am looking forward to seeing where it leads.
