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

  def test_expressions_arithmetic(self):
    v10 = expr.Literal(10)
    v3 = expr.Literal(3)
    
    # Add
    self.assertEqual(expr.Add(v10, v3).evaluate(self.cpu), 13)
    # Sub
    self.assertEqual(expr.Sub(v10, v3).evaluate(self.cpu), 7)
    # Mul
    self.assertEqual(expr.Mul(v10, v3).evaluate(self.cpu), 30)
    # Div
    self.assertEqual(expr.Div(v10, v3).evaluate(self.cpu), 3)
    # Mod
    self.assertEqual(expr.Mod(v10, v3).evaluate(self.cpu), 1)


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

    # Print expression
    p_expr = instr.PrintExpression(expr.Add(expr.Literal(10), expr.Literal(20)), "add(10, 20)")
    f = io.StringIO()
    with redirect_stdout(f):
      p_expr.execute(self.cpu)
    output = f.getvalue()
    self.assertIn("[DEBUG] add(10, 20) = 30 (0x0000001E)", output)


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

    # Print expression parsing
    prog_pexpr = "@print add(x1, 5)"
    instrs = parser.parse_program(prog_pexpr)
    pexpr_instr = instrs[0][0]
    self.assertIsInstance(pexpr_instr, instr.PrintExpression)
    self.assertEqual(pexpr_instr.expr_str, "add(x1, 5)")
    self.assertIsInstance(pexpr_instr.expr_obj, expr.Add)

  def test_parser_arithmetic_edge_cases(self):
    parser = Parser()
    
    # Whitespace handling
    instrs = parser.parse_program("@print add(  x1  ,   10  )")
    # The instruction is wrapped in a list of instructions for that address
    # structure: {addr: [instr, ...]}
    # Since we don't have addresses in the string, addr starts at 0
    # But wait, parse_program returns a dict {addr: [inst]}
    # Let's check the first instruction of the first address
    first_addr = list(instrs.keys())[0]
    self.assertIsInstance(instrs[first_addr][0], instr.PrintExpression)
    
    # Nested whitespace
    instrs = parser.parse_program("@print add( sub( x1, 1 ), 5 )")
    # Case insensitivity for operators
    instrs = parser.parse_program("@print ADD(x1, 5)")
    self.assertIsInstance(instrs[0][0], instr.PrintExpression)

  def test_functional_runtime_validation(self):
    """
    Simulates a "theory of language" test where the assembly code itself
    verifies the emulator's logic using @assert and @print.
    """
    program = """
    # Setup values
    li t0, 10
    li t1, 20
    li t2, 30
    
    # Verify basic arithmetic
    @assert eq(add(t0, t1), 30)
    @assert eq(sub(t1, t0), 10)
    @assert eq(mul(t0, t1), 200)
    @assert eq(div(t1, t0), 2)
    @assert eq(mod(t2, t1), 10)
    
    # Verify complex nesting
    # (10 + 20) * (30 - 20) = 30 * 10 = 300
    @assert eq(mul(add(t0, t1), sub(t2, t1)), 300)
    
    # Verify memory access with arithmetic address
    li sp, 0x1000
    sw t2, 4(sp)  # store 30 at sp+4
    
    # Check memory value using arithmetic expression for address
    @assert eq(m[add(sp, 4), u32], 30)
    
    # Check that @print doesn't crash (capture output)
    @print m[add(sp, 4), u32]
    @print add(t0, t1)
    """
    
    parser = Parser()
    instructions = parser.parse_program(program)
    
    # Execute
    # We need to flatten the instruction dictionary to a list for sequential execution test
    # but the CPU executes from memory. So let's load it into CPU.
    
    # Re-initialize CPU for this functional test
    self.cpu = CPU(mem_size=8192)
    
    # Load instructions into memory
    for addr, inst_list in instructions.items():
        for i, inst in enumerate(inst_list):
             # in a real run, we'd encode bytes, but here we execute objects directly
             # or we can manually step.
             # The CPU class doesn't have a direct "load objects" method for execution loop
             # without encoding. 
             # Let's manually run the meta-instructions and "execute" the real ones.
             pass
             
    # Actually, simpler: just iterate through sorted instructions and execute them
    # This mimics the fetch-decode-execute cycle for the purpose of testing the instruction logic
    
    sorted_addrs = sorted(instructions.keys())
    # Mock CPU state slightly for the flow
    self.cpu.pc = 0
    
    f = io.StringIO()
    with redirect_stdout(f):
        for addr in sorted_addrs:
            inst_list = instructions[addr]
            for inst in inst_list:
                inst.execute(self.cpu)
                
    output = f.getvalue()
    
    # Verify @print output
    self.assertIn("m[add(sp, 4), u32] = 30", output)
    self.assertIn("add(t0, t1) = 30", output)
    
    # Verify final state
    self.assertEqual(self.cpu.registers[5], 10) # t0
    self.assertEqual(self.cpu.registers[6], 20) # t1
    self.assertEqual(self.cpu.registers[7], 30) # t2
    val = self.cpu.memory.read(0x1004, 4)
    self.assertEqual(val, 30)



if __name__ == '__main__':
  unittest.main()
