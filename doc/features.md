RISC-V 32I Emulator: Comprehensive Feature Documentation

1. Core Integer Instruction Set (RV32I)
   The emulator implements the standard 32-bit base integer instruction set.

   1.1. Computational Instructions (Register-Register)
        - add: Performs 32-bit addition of two registers.
        - sub: Performs 32-bit subtraction of two registers.
        - sll: Logical left shift of a register by a register-specified amount.
        - slt: Sets the destination register to 1 if rs1 < rs2 (signed comparison), else 0.
        - sltu: Sets the destination register to 1 if rs1 < rs2 (unsigned comparison), else 0.
        - xor: Performs bitwise XOR of two registers.
        - srl: Logical right shift of a register by a register-specified amount.
        - sra: Arithmetic right shift of a register by a register-specified amount.
        - or: Performs bitwise OR of two registers.
        - and: Performs bitwise AND of two registers.

    1.2. M-Extension (Standard Extension for Integer Multiplication)
         - mul: Performs 32-bit integer multiplication of two registers (low 32 bits).

    1.3. Computational Instructions (Register-Immediate)
        - addi: Adds a sign-extended 12-bit immediate to a register.
        - slti: Sets to 1 if rs1 < immediate (signed comparison).
        - sltiu: Sets to 1 if rs1 < immediate (immediate is sign-extended then treated as unsigned).
        - xori: Performs bitwise XOR with a sign-extended 12-bit immediate.
        - ori: Performs bitwise OR with a sign-extended 12-bit immediate.
        - andi: Performs bitwise AND with a sign-extended 12-bit immediate.
        - slli: Logical left shift by a 5-bit immediate shift amount.
        - srli: Logical right shift by a 5-bit immediate shift amount.
        - srai: Arithmetic right shift by a 5-bit immediate shift amount.

   1.4. Memory Access Instructions
        - lw: Loads a 32-bit word from memory into a register.
        - lh: Loads a 16-bit halfword, sign-extends to 32 bits.
        - lhu: Loads a 16-bit halfword, zero-extends to 32 bits.
        - lb: Loads an 8-bit byte, sign-extends to 32 bits.
        - lbu: Loads an 8-bit byte, zero-extends to 32 bits.
        - sw: Stores a 32-bit word from a register to memory.
        - sh: Stores a 16-bit halfword from a register to memory.
        - sb: Stores an 8-bit byte from a register to memory.

   1.5. Control Transfer Instructions
        - beq: Branch if rs1 and rs2 are equal.
        - bne: Branch if rs1 and rs2 are not equal.
        - blt: Branch if rs1 < rs2 (signed comparison).
        - bge: Branch if rs1 >= rs2 (signed comparison).
        - bltu: Branch if rs1 < rs2 (unsigned comparison).
        - bgeu: Branch if rs1 >= rs2 (unsigned comparison).
        - lui: Load Upper Immediate; places a 20-bit immediate in the top 20 bits of the destination.
        - auipc: Add Upper Immediate to PC; adds a 20-bit immediate (shifted left 12) to the current PC.
        - jal: Jump and Link; adds a 20-bit relative offset to the PC and stores the return address (PC+4) in rd.
        - jalr: Jump and Link Register; jumps to rs1 + immediate and stores the return address (PC+4) in rd.

   1.6. System Instructions
        - fence: Provides ordering between memory/I/O accesses (currently implemented as a no-op).
        - ecall: Executes a system environment call. Supports:
          - a7=1: Print Integer (from a0)
          - a7=4: Print String (null-terminated from address in a0)
          - a7=10: Exit program (silent)
        - ebreak: Used to return control to a debugger (triggers halt).

2. Pseudo-Instructions and Directives
   Advanced assembly patterns and directives that control memory layout and instruction expansion.

   2.1. Memory and Layout Directives
        - .text: Switches to the code segment (base address 0x0000).
        - .data: Switches to the data segment (base address 0x4000).
        - .word: Reserves and initializes 32-bit words in the current segment.
        - .string: Reserves and initializes null-terminated strings.

   2.2. Basic register and value manipulation
        - li: Load Immediate; simplifies loading small or large constants.
        - mv: Move; copies the value of one register to another.
        - neg: Negate; computes the two's complement of a register value.
        - not: Bitwise NOT; computes the bitwise inverse of a register value.
        - nop: No Operation; does nothing for one cycle.

   2.3. Control Flow Pseudos
        - j: Unconditional jump to a relative target.
        - jr: Jump to an address stored in a register.
        - ret: Return from subroutine (jumps to address in 'ra' register).
        - call: External function call; uses auipc and jalr for large range.
        - la: Load Address; uses auipc and addi for PC-relative symbol resolution.

   2.4. Specialized Comparisons and Branches
        - seqz: Set if equal to zero.
        - snez: Set if not equal to zero.
        - sltz: Set if less than zero.
        - sgtz: Set if greater than zero.
        - beqz / bnez: Branch if value is / is not zero.
        - blez / bgez: Branch if value is <= / >= zero.
        - bltz / bgtz: Branch if value is < / > zero.
        - bgt / ble: Branch if greater / less or equal (swaps rs1/rs2 of blt/bge).
        - bgtu / bleu: Unsigned branch if greater / less or equal.

3. Debugging and Meta-Syntax
   The emulator includes a powerful meta-language for inspection during execution.

   3.1. Inspection Directives
        - @print: Outputs the value of a register, PC, or evaluated expression to the console.
        - @print_mem: Displays a range of memory with specific formatting (u8, s8, u16, s16, u32, s32).

   3.2. Verification Directives
        - @assert: Verifies a condition at runtime using the expression engine. Failure results in a halt.

   3.3. Expression Engine Capabilities
        - Arithmetic Operations: add(x, y), sub(x, y), mul(x, y), div(x, y), mod(x, y).
        - Boolean Comparisons: eq(x, y), ne(x, y), lt(x, y), gt(x, y), le(x, y), ge(x, y).
        - Logical Operators: and(a, b), or(a, b), not(a).
        - Data Accessors: pc, global registers (x0-x31), and memory indexing m[address, type].

4. System Architecture and Safety Features
   4.1. Register Management
        - 32-bit General Purpose Registers: Standard RISC-V x0-x31.
        - ABI Names: Supports standard aliases (ra, sp, gp, tp, t0-t6, s0-s11, a0-a7).
        - Zero Register: x0 is hardwired to 0 and cannot be written.

   4.2. Memory and Execution
        - Addressing: Byte-addressable memory access.
        - Segments: Code at 0x0000, Data at 0x4000. Safeguard against code-into-data collision.
        - Flow Control: Program Counter (PC) tracking and label resolution.

   4.3. Stack Safety Mechanism
        - Dynamic Checks: Runtime overflow and underflow protection.
        - Activation: Checks are active only when the 'sp' alias is used in assembly instructions.
        - Purpose: Ensures stack pointer remains within configured memory boundaries (default: base at 64KB, limit at 32KB).
