
import unittest
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cpu import CPU
from parser import Parser

class TestStackProtection(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.parser = Parser()

    def run_check(self, code, setup_sp=None):
        self.cpu.reset()
        if setup_sp is not None:
            self.cpu.registers['sp'] = setup_sp
        
        # Parse
        instructions = self.parser.parse_program(code)
        
        # Execute
        self.cpu.step(instructions)
        return self.cpu.halted

    def test_sp_overflow(self):
        # sp starts at stack_base (65536)
        # Limit is 32768
        # Setting sp to limit - 4 should trigger overflow
        self.cpu.registers['sp'] = 32770
        code = "addi sp, sp, -4"
        
        instructions = self.parser.parse_program(code)
        # Check if parsed instruction has 'use_sp' tag
        instr_obj = instructions[0][0] 
        self.assertIn("use_sp", instr_obj.tags)
        
        self.cpu.step(instructions)
        self.assertTrue(self.cpu.halted, "CPU should halt on stack overflow with sp alias")

    def test_x2_no_overflow(self):
        self.cpu.registers['x2'] = 32770
        code = "addi x2, x2, -4"
        
        instructions = self.parser.parse_program(code)
        instr_obj = instructions[0][0]
        self.assertNotIn("use_sp", instr_obj.tags)
        
        self.cpu.step(instructions)
        
        self.assertFalse(self.cpu.halted)
        self.assertEqual(self.cpu.registers['x2'], 32766)

    def test_sp_underflow(self):
        self.cpu.registers['sp'] = 65536
        code = "addi sp, sp, 4"
        
        instructions = self.parser.parse_program(code)
        self.cpu.step(instructions)
        
        self.assertTrue(self.cpu.halted, "CPU should halt on stack underflow with sp alias")

    def test_x2_no_underflow(self):
        self.cpu.registers['x2'] = 65536
        code = "addi x2, x2, 4"
        
        instructions = self.parser.parse_program(code)
        self.cpu.step(instructions)
        
        self.assertFalse(self.cpu.halted)
        self.assertEqual(self.cpu.registers['x2'], 65540)
        
if __name__ == '__main__':
    unittest.main()
