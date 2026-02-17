"""
Unit tests for the Parser of the RISC-V emulator.
"""

import unittest
from parser import Parser
import instructions as instr

class TestParser(unittest.TestCase):
  def setUp(self):
    self.parser = Parser()

  def test_parse_r_type(self):
    program = "add x1, x2, x3"
    parse_result = self.parser.parse_program(program)
    instrs = parse_result['instructions']
    self.assertIn(0, instrs)
    self.assertIsInstance(instrs[0][0], instr.Add)
    self.assertEqual(instrs[0][0].rd, 1)
    self.assertEqual(instrs[0][0].rs1, 2)
    self.assertEqual(instrs[0][0].rs2, 3)

  def test_pseudo_instructions(self):
    program = "li x1, 0x12345678\nmv x2, x1\nnop"
    parse_result = self.parser.parse_program(program)
    instrs = parse_result['instructions']
    self.assertIsInstance(instrs[0][0], instr.Lui)
    self.assertIsInstance(instrs[4][0], instr.Addi)
    self.assertIsInstance(instrs[8][0], instr.Addi) # mv
    self.assertIsInstance(instrs[12][0], instr.Addi) # nop

  def test_complex_expressions(self):
    program = "@assert and(eq(x1, 5), not(lt(m[0, u32], 100)))"
    parse_result = self.parser.parse_program(program)
    instrs = parse_result['instructions']
    self.assertIsInstance(instrs[0][0], instr.Assert)
    expr = instrs[0][0].expression_tree
    self.assertEqual(expr.__class__.__name__, "AndExpr")

  def test_varied_whitespace(self):
    program = "  add  x1,x2,  x3  # comment\n\n  @print   x1  "
    parse_result = self.parser.parse_program(program)
    instrs = parse_result['instructions']
    self.assertIn(0, instrs)
    self.assertIn(4, instrs)

  def test_labels(self):
    program = """
    loop:
      addi x1, x1, 1
      beq x1, x2, loop
    """
    parse_result = self.parser.parse_program(program)
    instrs = parse_result['instructions']
    self.assertEqual(self.parser.labels['loop'], 0)
    self.assertEqual(instrs[4][0].imm, -4) # Relative offset from PC=4 to PC=0

  def test_jal_shorthand(self):
    program = "jal target\ntarget: addi x0, x0, 0"
    self.parser.parse_program(program)
    self.assertEqual(self.parser.labels['target'], 4)

  def test_jalr_formats(self):
    # jalr rd, rs1, imm
    parse_result = self.parser.parse_program("jalr x1, x2, 10")
    instrs = parse_result['instructions']
    self.assertIsInstance(instrs[0][0], instr.Jalr)
    
    # jalr rd, imm(rs1)
    self.parser = Parser()
    parse_result = self.parser.parse_program("jalr x1, 10(x2)")
    instrs = parse_result['instructions']
    self.assertIsInstance(instrs[0][0], instr.Jalr)

  def test_meta_syntax(self):
    program = "@assert eq(x1, 5)\n@print x1\n@print_mem 0x100 u32 4"
    parse_result = self.parser.parse_program(program)
    instrs = parse_result['instructions']
    self.assertIsInstance(instrs[0][0], instr.Assert)
    self.assertIsInstance(instrs[4][0], instr.Print)
    self.assertIsInstance(instrs[8][0], instr.PrintMem)

  def test_invalid_syntax(self):
    with self.assertRaises(Exception):
      self.parser.parse_program("invalid_mnemonic x1, x2")
    with self.assertRaises(Exception):
      self.parser.parse_program("add x1, x2") # Missing arg

if __name__ == '__main__':
  unittest.main()
