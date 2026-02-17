import unittest
import sys
from io import StringIO
from cpu import CPU
import instructions as instr

class TestSyscalls(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU(mem_size=1024)
        self.held_output = StringIO()
        self.old_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = self.old_stdout

    def test_syscall_print_int(self):
        # Syscall 1: Print Integer
        self.cpu.registers[17] = 1 # a7
        self.cpu.registers[10] = 1234 # a0
        instr.Ecall().execute(self.cpu)
        self.assertEqual(self.held_output.getvalue(), "1234")

    def test_syscall_print_int_negative(self):
        # Syscall 1: Print Integer (Negative)
        self.cpu.registers[17] = 1 # a7
        self.cpu.registers[10] = 0xFFFFFFFF # -1
        instr.Ecall().execute(self.cpu)
        self.assertEqual(self.held_output.getvalue(), "-1")

    def test_syscall_print_string(self):
        # Syscall 4: Print String
        addr = 0x100
        s = "Hello, World!"
        for i, char in enumerate(s):
            self.cpu.memory.write_byte(addr + i, ord(char))
        self.cpu.memory.write_byte(addr + len(s), 0) # Null terminator

        self.cpu.registers[17] = 4 # a7
        self.cpu.registers[10] = addr # a0
        instr.Ecall().execute(self.cpu)
        self.assertEqual(self.held_output.getvalue(), "Hello, World!")

    def test_syscall_exit(self):
        # Syscall 10: Exit
        self.cpu.registers[17] = 10 # a7
        self.cpu.registers[10] = 0 # a0
        self.assertFalse(self.cpu.halted)
        instr.Ecall().execute(self.cpu)
        self.assertTrue(self.cpu.halted)

    def test_unknown_syscall(self):
        # Unknown Syscall
        self.cpu.registers[17] = 99 # a7
        instr.Ecall().execute(self.cpu)
        self.assertTrue(self.cpu.halted)
        self.assertIn("Unknown syscall: 99", self.held_output.getvalue())

if __name__ == '__main__':
    unittest.main()
