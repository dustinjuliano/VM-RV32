# VM-RV32: RISC-V 32I Assembly Emulator

An educational tool for learning RISC-V assembly programming through simulation, meta-syntax debugging, and formal verification. This project provides a minimalist environment for understanding the RV32I Instruction Set Architecture (ISA) and the RISC-V Calling Convention.

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

The project includes a comprehensive series of **64 tutorials** designed to guide a learner from zero knowledge to a deep understanding of the RISC-V 32I ISA:

1. **Basic Mechanics**: Instructions, immediates, and bitwise operations.
2. **Memory & Control**: Loads, stores, branches, and jumps.
3. **The ABI**: Understanding register roles and the calling convention.
4. **Stack & Frames**: Managing memory for function calls.
5. **Pseudo-instructions**: Mastering the standard abstractions.
6. **Verification Pro**: Advanced use of the emulator's meta-syntax.

## Verification & Testing

Every part of this project is rigorously tested to ensure architectural accuracy and reliability. Our test suite includes over **150 automated test cases**, covering:
- **Instruction Specification**: Every RV32I instruction is verified against formal state transitions.
- **Parser & Meta-syntax**: Robust validation of assembly parsing and the `@assert` expression engine.
- **Tutorial Logic**: Every tutorial file is executed and validated in a dedicated test suite that verifies the specific end-state and logic of the lesson.

To run the full test suite:
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
