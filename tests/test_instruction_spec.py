"""
Formal Instruction Specification Test Suite for RV32I.
Verifies every instruction against expected state transitions.
"""

import unittest
from cpu import CPU
import instructions as instr

class TestInstructionSpec(unittest.TestCase):
  def setUp(self):
    self.cpu = CPU(mem_size=4096)

  def run_spec(self, name, setup_func, instruction, expected_regs=None, expected_pc=None, expected_mem=None):
    """
    Helper to run a formal specification test case.
    """
    # 1. Setup
    setup_func(self.cpu)
    initial_pc = self.cpu.pc
    
    # 2. Execute
    # We simulate a "step" by calling execute directly
    new_pc = instruction.execute(self.cpu)
    
    # instructions.py:execute returns new_pc if it jumps/branches, else None.
    # The CPU loop handles this. Let's mimic that logic here.
    if new_pc is not None:
      self.cpu.pc = new_pc
    else:
      self.cpu.pc += 4

    # 3. Verify
    if expected_pc is not None:
      self.assertEqual(self.cpu.pc, expected_pc, f"[{name}] PC mismatch")
    
    if expected_regs:
      for reg, val in expected_regs.items():
        self.assertEqual(self.cpu.registers[reg], val & 0xFFFFFFFF, f"[{name}] x{reg} mismatch")
        
    if expected_mem:
      for addr, (val, type_str) in expected_mem.items():
        self.assertEqual(self.cpu.memory.read_typed(addr, type_str), val, f"[{name}] Mem at 0x{addr:X} mismatch")

  # --- R-Type ---
  def test_add(self):
    def setup(cpu):
      cpu.registers[1] = 0x12345678
      cpu.registers[2] = 0x00000001
    self.run_spec("ADD", setup, instr.Add(3, 1, 2), expected_regs={3: 0x12345679})
    
    # 32-bit overflow
    def setup_ovf(cpu):
      cpu.registers[1] = 0x7FFFFFFF
      cpu.registers[2] = 1
    self.run_spec("ADD_OVF", setup_ovf, instr.Add(3, 1, 2), expected_regs={3: 0x80000000})

  def test_sub(self):
    def setup(cpu):
      cpu.registers[1] = 0x00000010
      cpu.registers[2] = 0x00000011
    self.run_spec("SUB", setup, instr.Sub(3, 1, 2), expected_regs={3: 0xFFFFFFFF})
    
    # Large SUB
    def setup_large(cpu):
      cpu.registers[1] = 0
      cpu.registers[2] = 1
    self.run_spec("SUB_UNDER", setup_large, instr.Sub(3, 1, 2), expected_regs={3: 0xFFFFFFFF})

  def test_sll(self):
    def setup(cpu):
      cpu.registers[1] = 0x00000001
      cpu.registers[2] = 5
    self.run_spec("SLL", setup, instr.Sll(3, 1, 2), expected_regs={3: 0x00000020})
    
    # Shift by more than 31 (should use rs2[4:0])
    def setup_mask(cpu):
      cpu.registers[1] = 1
      cpu.registers[2] = 33
    self.run_spec("SLL_MASK", setup_mask, instr.Sll(3, 1, 2), expected_regs={3: 2})

  def test_slt(self):
    def setup(cpu):
      cpu.registers[1] = 0xFFFFFFFF # -1
      cpu.registers[2] = 1
    self.run_spec("SLT", setup, instr.Slt(3, 1, 2), expected_regs={3: 1})
    
    # Negative vs Negative
    def setup_neg(cpu):
      cpu.registers[1] = 0xFFFFFFFE # -2
      cpu.registers[2] = 0xFFFFFFFF # -1
    self.run_spec("SLT_NEG", setup_neg, instr.Slt(3, 1, 2), expected_regs={3: 1})

  def test_sltu(self):
    def setup(cpu):
      cpu.registers[1] = 0xFFFFFFFF
      cpu.registers[2] = 1
    self.run_spec("SLTU", setup, instr.Sltu(3, 1, 2), expected_regs={3: 0})

  def test_xor(self):
    def setup(cpu):
      cpu.registers[1] = 0xAA
      cpu.registers[2] = 0x55
    self.run_spec("XOR", setup, instr.Xor(3, 1, 2), expected_regs={3: 0xFF})

  def test_srl(self):
    def setup(cpu):
      cpu.registers[1] = 0x80000000
      cpu.registers[2] = 1
    self.run_spec("SRL", setup, instr.Srl(3, 1, 2), expected_regs={3: 0x40000000})

  def test_sra(self):
    def setup(cpu):
      cpu.registers[1] = 0x80000000
      cpu.registers[2] = 1
    self.run_spec("SRA", setup, instr.Sra(3, 1, 2), expected_regs={3: 0xC0000000})

  def test_or(self):
    def setup(cpu):
      cpu.registers[1] = 0x0F
      cpu.registers[2] = 0xF0
    self.run_spec("OR", setup, instr.Or(3, 1, 2), expected_regs={3: 0xFF})

  def test_and(self):
    def setup(cpu):
      cpu.registers[1] = 0x01
      cpu.registers[2] = 0x03
    self.run_spec("AND", setup, instr.And(3, 1, 2), expected_regs={3: 0x01})

  # --- I-Type (ALU) ---
  def test_addi(self):
    def setup(cpu):
      cpu.registers[1] = 0x10
    self.run_spec("ADDI", setup, instr.Addi(2, 1, -5), expected_regs={2: 0x0B})
    
    # Max positive imm (2047)
    self.run_spec("ADDI_MAX", setup, instr.Addi(2, 1, 2047), expected_regs={2: 2063})

  def test_slti(self):
    def setup(cpu):
      cpu.registers[1] = -10
    self.run_spec("SLTI", setup, instr.Slti(2, 1, -5), expected_regs={2: 1})

  def test_sltiu(self):
    def setup(cpu):
      cpu.registers[1] = 10
    self.run_spec("SLTIU", setup, instr.Sltiu(2, 1, -1), expected_regs={2: 1}) # 10 < 0xFFFFFFFF

  def test_xori(self):
    def setup(cpu):
      cpu.registers[1] = 0xAA
    self.run_spec("XORI", setup, instr.Xori(2, 1, 0x55), expected_regs={2: 0xFF})

  def test_ori(self):
    def setup(cpu):
      cpu.registers[1] = 0x0F
    self.run_spec("ORI", setup, instr.Ori(2, 1, 0xF0), expected_regs={2: 0xFF})

  def test_andi(self):
    def setup(cpu):
      cpu.registers[1] = 0x03
    self.run_spec("ANDI", setup, instr.Andi(2, 1, 0x01), expected_regs={2: 0x01})

  def test_slli(self):
    def setup(cpu):
      cpu.registers[1] = 0x1
    self.run_spec("SLLI", setup, instr.Slli(2, 1, 4), expected_regs={2: 0x10})

  def test_srli(self):
    def setup(cpu):
      cpu.registers[1] = 0x10
    self.run_spec("SRLI", setup, instr.Srli(2, 1, 4), expected_regs={2: 0x1})

  def test_srai(self):
    def setup(cpu):
      cpu.registers[1] = 0x80000000
    self.run_spec("SRAI", setup, instr.Srai(2, 1, 4), expected_regs={2: 0xF8000000})

  # --- Load/Store ---
  def test_lw_sw(self):
    def setup(cpu):
      cpu.registers[1] = 100
      cpu.registers[2] = 0xDEADBEEF
    self.run_spec("SW", setup, instr.Sw(1, 2, 4), expected_mem={104: (0xDEADBEEF, "u32")})
    
    def setup_load(cpu):
      cpu.registers[1] = 100
      cpu.memory.write(104, 4, 0xCAFEBABE)
    self.run_spec("LW", setup_load, instr.Lw(3, 1, 4), expected_regs={3: 0xCAFEBABE})

  def test_sb_sh(self):
    def setup(cpu):
      cpu.registers[1] = 100
      cpu.registers[2] = 0x12345678
    self.run_spec("SB", setup, instr.Sb(1, 2, 0), expected_mem={100: (0x78, "u8")})
    self.run_spec("SH", setup, instr.Sh(1, 2, 2), expected_mem={102: (0x5678, "u16")})

  def test_lh_lb(self):
    def setup(cpu):
      cpu.memory.write(100, 4, 0x000080FF) # Byte 0: FF, Byte 1: 80
    # LB: signed FF -> -1
    self.run_spec("LB", setup, instr.Lb(1, 0, 100), expected_regs={1: 0xFFFFFFFF})
    # LBU: unsigned FF -> 255
    self.run_spec("LBU", setup, instr.Lbu(1, 0, 100), expected_regs={1: 255})
    # LH: signed 80FF -> -32513
    self.run_spec("LH", setup, instr.Lh(1, 0, 100), expected_regs={1: 0xFFFF80FF})
    # LHU: unsigned 80FF -> 33023
    self.run_spec("LHU", setup, instr.Lhu(1, 0, 100), expected_regs={1: 0x80FF})

  # --- Control Flow ---
  def test_beq(self):
    def setup(cpu):
      cpu.pc = 100
      cpu.registers[1] = 10
      cpu.registers[2] = 10
    self.run_spec("BEQ_TAKEN", setup, instr.Beq(1, 2, 40), expected_pc=140)
    
    def setup_not(cpu):
      cpu.pc = 100
      cpu.registers[1] = 10
      cpu.registers[2] = 11
    self.run_spec("BEQ_NOT_TAKEN", setup_not, instr.Beq(1, 2, 40), expected_pc=104)

  def test_bne(self):
    def setup(cpu):
      cpu.pc = 100
      cpu.registers[1] = 10
      cpu.registers[2] = 11
    self.run_spec("BNE_TAKEN", setup, instr.Bne(1, 2, 40), expected_pc=140)

  def test_blt(self):
    def setup(cpu):
      cpu.pc = 100
      cpu.registers[1] = -10
      cpu.registers[2] = 10
    self.run_spec("BLT_TAKEN", setup, instr.Blt(1, 2, 40), expected_pc=140)
    
    def setup_not(cpu):
      cpu.pc = 100
      cpu.registers[1] = 10
      cpu.registers[2] = -10
    self.run_spec("BLT_NOT_TAKEN", setup_not, instr.Blt(1, 2, 40), expected_pc=104)

  def test_bge(self):
    def setup(cpu):
      cpu.pc = 100
      cpu.registers[1] = 10
      cpu.registers[2] = 5
    self.run_spec("BGE_TAKEN", setup, instr.Bge(1, 2, 40), expected_pc=140)

  def test_bltu(self):
    def setup(cpu):
      cpu.pc = 100
      cpu.registers[1] = 10
      cpu.registers[2] = 0xFFFFFFFF
    self.run_spec("BLTU_TAKEN", setup, instr.Bltu(1, 2, 40), expected_pc=140)

  def test_bgeu(self):
    def setup(cpu):
      cpu.pc = 100
      cpu.registers[1] = 0xFFFFFFFF
      cpu.registers[2] = 10
    self.run_spec("BGEU_TAKEN", setup, instr.Bgeu(1, 2, 40), expected_pc=140)

  def test_lui_auipc(self):
    self.run_spec("LUI", lambda cpu: None, instr.Lui(1, 0x12345), expected_regs={1: 0x12345000})
    def setup_auipc(cpu):
      cpu.pc = 0x1000
    self.run_spec("AUIPC", setup_auipc, instr.Auipc(1, 0x12345), expected_regs={1: 0x12346000}, expected_pc=0x1004)

  def test_jal_jalr(self):
    def setup_jal(cpu):
      cpu.pc = 100
    self.run_spec("JAL", setup_jal, instr.Jal(1, 100), expected_pc=200, expected_regs={1: 104})
    
    def setup_jalr(cpu):
      cpu.pc = 100
      cpu.registers[2] = 500
    self.run_spec("JALR", setup_jalr, instr.Jalr(1, 2, 10), expected_pc=510, expected_regs={1: 104})
    
    # JALR with negative offset
    def setup_jalr_neg(cpu):
      cpu.pc = 500
      cpu.registers[2] = 500
    self.run_spec("JALR_NEG", setup_jalr_neg, instr.Jalr(1, 2, -100), expected_pc=400, expected_regs={1: 504})

if __name__ == '__main__':
  unittest.main()
