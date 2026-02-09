"""
Unit tests for the CPU, RegisterFile, and Instructions of the RISC-V emulator.
Aims for 100% code coverage.
"""

import unittest
from cpu import CPU
from registers import RegisterFile
from memory import Memory
import instructions as instr
import expressions as expr

class TestCore(unittest.TestCase):
  def setUp(self):
    self.cpu = CPU(mem_size=1024)

  def test_register_zero(self):
    # x0 is hardwired to 0
    self.cpu.registers[0] = 100
    self.assertEqual(self.cpu.registers[0], 0)
    
  def test_register_range(self):
    # Check that we have exactly 32 registers
    self.cpu.registers[31] = 0xAA
    self.assertEqual(self.cpu.registers[31], 0xAA)
    with self.assertRaises(IndexError):
      _ = self.cpu.registers[32]

  def test_register_alias(self):
    # Check common aliases
    self.cpu.registers[1] = 0x123
    self.assertEqual(self.cpu.registers['ra'], 0x123)
    self.cpu.registers['sp'] = 0x456
    self.assertEqual(self.cpu.registers[2], 0x456)

  def test_cpu_reset(self):
    self.cpu.registers[1] = 100
    self.cpu.pc = 200
    self.cpu.halted = True
    self.cpu.reset()
    self.assertEqual(self.cpu.registers[1], 0)
    self.assertEqual(self.cpu.pc, 0)
    self.assertFalse(self.cpu.halted)

  def test_cpu_step_error(self):
    # No instruction at PC
    self.cpu.pc = 0x1234
    self.cpu.step({})
    self.assertTrue(self.cpu.halted)

  def test_arithmetic(self):
    # ADD
    self.cpu.registers[1] = 0x7FFFFFFF
    self.cpu.registers[2] = 1
    instr.Add(3, 1, 2).execute(self.cpu)
    self.assertEqual(self.cpu.registers[3], 0x80000000)
    
    # SUB (overflow case)
    self.cpu.registers[1] = 0
    self.cpu.registers[2] = 1
    instr.Sub(3, 1, 2).execute(self.cpu)
    self.assertEqual(self.cpu.registers[3], 0xFFFFFFFF)

    # XOR, OR, AND
    self.cpu.registers[1] = 0b1010
    self.cpu.registers[2] = 0b1100
    instr.Xor(3, 1, 2).execute(self.cpu)
    self.assertEqual(self.cpu.registers[3], 0b0110)
    instr.Or(3, 1, 2).execute(self.cpu)
    self.assertEqual(self.cpu.registers[3], 0b1110)
    instr.And(3, 1, 2).execute(self.cpu)
    self.assertEqual(self.cpu.registers[3], 0b1000)

  def test_shifts(self):
    # SLL (logical left)
    self.cpu.registers[1] = 0xFFFF0000
    self.cpu.registers[2] = 4
    instr.Sll(3, 1, 2).execute(self.cpu)
    self.assertEqual(self.cpu.registers[3], 0xFFF00000)
    
    # SRL (logical right)
    self.cpu.registers[1] = 0x80000000
    self.cpu.registers[2] = 1
    instr.Srl(3, 1, 2).execute(self.cpu)
    self.assertEqual(self.cpu.registers[3], 0x40000000)
    
    # SRA (arithmetic right - sign extension)
    self.cpu.registers[1] = 0x80000000
    self.cpu.registers[2] = 1
    instr.Sra(3, 1, 2).execute(self.cpu)
    self.assertEqual(self.cpu.registers[3], 0xC0000000)
    
    # SRA (positive case)
    self.cpu.registers[1] = 0x40000000
    self.cpu.registers[2] = 1
    instr.Sra(3, 1, 2).execute(self.cpu)
    self.assertEqual(self.cpu.registers[3], 0x20000000)

  def test_comparisons(self):
    # SLT (signed)
    self.cpu.registers[1] = 0xFFFFFFFF # -1
    self.cpu.registers[2] = 1          # 1
    instr.Slt(3, 1, 2).execute(self.cpu)
    self.assertEqual(self.cpu.registers[3], 1)
    
    # SLTU (unsigned)
    instr.Sltu(3, 1, 2).execute(self.cpu)
    self.assertEqual(self.cpu.registers[3], 0) # 0xFFFFFFFF > 1

  def test_immediate_arithmetic(self):
    self.cpu.registers[1] = 10
    instr.Addi(3, 1, 20).execute(self.cpu)
    self.assertEqual(self.cpu.registers[3], 30)
    
    instr.Slti(3, 1, 0).execute(self.cpu) # 10 < 0 -> 0
    self.assertEqual(self.cpu.registers[3], 0)
    
    instr.Slti(3, 1, 20).execute(self.cpu) # 10 < 20 -> 1
    self.assertEqual(self.cpu.registers[3], 1)
    
    # SLTIU (sign-extended imm then unsigned compare)
    instr.Sltiu(3, 1, -1).execute(self.cpu) # 10 < 0xFFFFFFFF -> 1
    self.assertEqual(self.cpu.registers[3], 1)

  def test_control_flow(self):
    # BEQ (taken)
    self.cpu.pc = 100
    self.cpu.registers[1] = 10
    self.cpu.registers[2] = 10
    new_pc = instr.Beq(1, 2, 40).execute(self.cpu)
    self.assertEqual(new_pc, 140)
    
    # BNE (not taken)
    new_pc = instr.Bne(1, 2, 40).execute(self.cpu)
    self.assertIsNone(new_pc)
    
    # JAL
    self.cpu.pc = 200
    new_pc = instr.Jal(1, 100).execute(self.cpu)
    self.assertEqual(new_pc, 300)
    self.assertEqual(self.cpu.registers[1], 204)
    
    # JALR
    self.cpu.pc = 200
    self.cpu.registers[2] = 500
    new_pc = instr.Jalr(1, 2, 10).execute(self.cpu)
    self.assertEqual(new_pc, 510)
    self.assertEqual(self.cpu.registers[1], 204)

  def test_u_type(self):
    # LUI
    instr.Lui(1, 0x12345).execute(self.cpu)
    self.assertEqual(self.cpu.registers[1], 0x12345000)
    
    # AUIPC
    self.cpu.pc = 0x1000
    instr.Auipc(1, 0x12345).execute(self.cpu)
    self.assertEqual(self.cpu.registers[1], 0x12345000 + 0x1000)

  def test_meta_print(self):
    # Just ensure it doesn't crash
    self.cpu.registers[1] = 42
    instr.Print("x1", 1).execute(self.cpu)
    
    self.cpu.memory.write(100, 4, 0x12345678)
    instr.PrintMem(100, "u32", 1).execute(self.cpu)

  def test_assertions(self):
    # Successful assertion
    self.cpu.registers[1] = 5
    assertion = instr.Assert(expr.Eq(expr.RegAccess(1), expr.Literal(5)), "eq(x1, 5)")
    assertion.execute(self.cpu)
    
    # Failed assertion
    with self.assertRaises(AssertionError):
      instr.Assert(expr.Eq(expr.RegAccess(1), expr.Literal(10)), "eq(x1, 10)").execute(self.cpu)
    self.assertTrue(self.cpu.halted)

  def test_complex_expressions(self):
    # and(eq(x1, 5), not(eq(x2, 0)))
    self.cpu.registers[1] = 5
    self.cpu.registers[2] = 10
    e = expr.AndExpr(
      expr.Eq(expr.RegAccess(1), expr.Literal(5)),
      expr.NotExpr(expr.Eq(expr.RegAccess(2), expr.Literal(0)))
    )
    self.assertTrue(e.evaluate(self.cpu))

    # ge, le, lt, gt, ne
    self.assertTrue(expr.Ge(expr.Literal(5), expr.Literal(5)).evaluate(self.cpu))
    self.assertTrue(expr.Le(expr.Literal(5), expr.Literal(5)).evaluate(self.cpu))
    self.assertTrue(expr.Lt(expr.Literal(4), expr.Literal(5)).evaluate(self.cpu))
    self.assertTrue(expr.Gt(expr.Literal(6), expr.Literal(5)).evaluate(self.cpu))
    self.assertTrue(expr.Ne(expr.Literal(5), expr.Literal(6)).evaluate(self.cpu))
    self.assertTrue(expr.OrExpr(expr.Literal(0), expr.Literal(1)).evaluate(self.cpu))

if __name__ == '__main__':
  unittest.main()
