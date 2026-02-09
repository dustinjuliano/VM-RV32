import unittest
from cpu import CPU
from parser import Parser
import instructions as instr

class TestStack(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU(mem_size=1024)
        self.parser = Parser()

    def test_sp_initialization(self):
        # sp should start at mem_size
        self.assertEqual(self.cpu.registers['sp'], 1024)
        
    def test_stack_overflow_protection(self):
        # Default stack limit is mem_size // 2 (512)
        # Moving sp below that should trigger a halt ONLY IF the instruction uses 'sp'
        
        # 1. Raw x2 should NOT trigger halt even if out of bounds
        self.cpu.registers['sp'] = 511
        nop_raw = instr.Add(0, 0, 0) # Raw instruction, no tags
        self.cpu.step({0: [nop_raw]})
        self.assertFalse(self.cpu.halted)
        
        # 2. Instruction with 'use_sp' tag SHOULD trigger halt
        nop_sp = instr.Add(0, 0, 0)
        nop_sp.tags.add("use_sp")
        self.cpu.step({4: [nop_sp]})
        self.assertTrue(self.cpu.halted)

    def test_stack_underflow_protection(self):
        # sp should not go above mem_size
        
        # 1. Raw x2 should NOT trigger halt
        self.cpu.registers['sp'] = 1025
        nop_raw = instr.Add(0, 0, 0)
        self.cpu.step({0: [nop_raw]})
        self.assertFalse(self.cpu.halted)
        
        # 2. Instruction with 'use_sp' tag SHOULD trigger halt
        nop_sp = instr.Add(0, 0, 0)
        nop_sp.tags.add("use_sp")
        self.cpu.step({4: [nop_sp]})
        self.assertTrue(self.cpu.halted)

    def test_abi_push_pop_simulation(self):
        # Test a manual push/pop sequence using 'sp' alias
        program = """
        addi sp, sp, -16
        sw   ra, 12(sp)
        lw   t0, 12(sp)
        addi sp, sp, 16
        """
        self.cpu.registers['ra'] = 0xDEADBEEF
        instrs = self.parser.parse_program(program)
        
        # Step through the 4 instructions
        for _ in range(4):
            self.cpu.step(instrs)
        
        self.assertEqual(self.cpu.registers['t0'], 0xDEADBEEF)
        self.assertEqual(self.cpu.registers['sp'], 1024)
        self.assertFalse(self.cpu.halted)

if __name__ == '__main__':
    unittest.main()
