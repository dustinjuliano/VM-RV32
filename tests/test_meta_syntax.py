"""
Comprehensive tests for Meta-Syntax (@assert, @print, @print_mem)
and the functional expression language.
"""

import unittest
from cpu import CPU
import instructions as instr
import expressions as expr
from parser import Parser
import io
from contextlib import redirect_stdout

class TestMetaSyntax(unittest.TestCase):
  def setUp(self):
    self.cpu = CPU(mem_size=1024)

  def test_expressions_basic(self):
    # Literal
    self.assertEqual(expr.Literal(10).evaluate(self.cpu), 10)
    
    # RegAccess
    self.cpu.registers[1] = 42
    self.assertEqual(expr.RegAccess(1).evaluate(self.cpu), 42)
    
    # MemAccess
    self.cpu.memory.write(100, 4, 0x12345678)
    self.assertEqual(expr.MemAccess(expr.Literal(100), "u32").evaluate(self.cpu), 0x12345678)
    self.assertEqual(expr.MemAccess(expr.Literal(100), "u8").evaluate(self.cpu), 0x78)

  def test_expressions_logical(self):
    true = expr.Literal(1)
    false = expr.Literal(0)
    
    # Not
    self.assertTrue(expr.NotExpr(false).evaluate(self.cpu))
    self.assertFalse(expr.NotExpr(true).evaluate(self.cpu))
    
    # And
    self.assertTrue(expr.AndExpr(true, true).evaluate(self.cpu))
    self.assertFalse(expr.AndExpr(true, false).evaluate(self.cpu))
    
    # Or
    self.assertTrue(expr.OrExpr(true, false).evaluate(self.cpu))
    self.assertFalse(expr.OrExpr(false, false).evaluate(self.cpu))

  def test_expressions_comparisons(self):
    v5 = expr.Literal(5)
    v10 = expr.Literal(10)
    
    self.assertTrue(expr.Eq(v5, v5).evaluate(self.cpu))
    self.assertTrue(expr.Ne(v5, v10).evaluate(self.cpu))
    self.assertTrue(expr.Lt(v5, v10).evaluate(self.cpu))
    self.assertTrue(expr.Le(v5, v5).evaluate(self.cpu))
    self.assertTrue(expr.Gt(v10, v5).evaluate(self.cpu))
    self.assertTrue(expr.Ge(v5, v5).evaluate(self.cpu))

  def test_assert_instruction(self):
    # Success
    self.cpu.registers[1] = 5
    a = instr.Assert(expr.Eq(expr.RegAccess(1), expr.Literal(5)), "eq(x1, 5)")
    a.execute(self.cpu)
    self.assertFalse(self.cpu.halted)
    
    # Failure
    a_fail = instr.Assert(expr.Eq(expr.RegAccess(1), expr.Literal(10)), "eq(x1, 10)")
    with self.assertRaises(AssertionError):
      a_fail.execute(self.cpu)
    self.assertTrue(self.cpu.halted)

  def test_print_instructions(self):
    # Print register
    self.cpu.registers[1] = 0xABC
    p_reg = instr.Print("x1", 1)
    
    f = io.StringIO()
    with redirect_stdout(f):
      p_reg.execute(self.cpu)
    output = f.getvalue()
    self.assertIn("x1 = 2748", output)
    self.assertIn("0x00000ABC", output)

    # Print memory
    self.cpu.memory.write(100, 4, 0x12345678)
    p_mem = instr.PrintMem(100, "u32", 1)
    
    f = io.StringIO()
    with redirect_stdout(f):
      p_mem.execute(self.cpu)
    output = f.getvalue()
    self.assertIn("0x00000064: 305419896", output)

  def test_parser_meta(self):
    # Deep check of parser's meta instruction generation
    parser = Parser()
    
    # Assert parsing
    prog = "@assert and(eq(x1, 5), ne(x2, 0))"
    instrs = parser.parse_program(prog)
    assert_instr = instrs[0][0]
    self.assertIsInstance(assert_instr, instr.Assert)
    self.assertEqual(assert_instr.line_text, "and(eq(x1, 5), ne(x2, 0))")
    
    # Print parsing
    prog_print = "@print x5"
    instrs = parser.parse_program(prog_print)
    print_instr = instrs[0][0]
    self.assertIsInstance(print_instr, instr.Print)
    self.assertEqual(print_instr.reg_name, "x5")
    
    # Print_mem parsing
    prog_pmem = "@print_mem 0x100 u16 8"
    instrs = parser.parse_program(prog_pmem)
    pm_instr = instrs[0][0]
    self.assertIsInstance(pm_instr, instr.PrintMem)
    self.assertEqual(pm_instr.addr_expr, 0x100)
    self.assertEqual(pm_instr.type_str, "u16")
    self.assertEqual(pm_instr.n, 8)

if __name__ == '__main__':
  unittest.main()
