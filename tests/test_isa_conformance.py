
import unittest
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cpu import CPU
from parser import Parser
import instructions as instr

class TestISAConformance(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.parser = Parser()

    def verify_mnemonic(self, mnemonic, args, expected_class):
        code = f"{mnemonic} {args}"
        try:
            parse_result = self.parser.parse_program(code)
            instructions = parse_result['instructions']
            # instructions is {addr: [obj]}
            obj = instructions[0][0]
            self.assertIsInstance(obj, expected_class, f"Checking {mnemonic}")
        except Exception as e:
            self.fail(f"Failed to parse {mnemonic}: {e}")

    def test_rv32i_base(self):
        # R-Type
        self.verify_mnemonic('add', 'x1, x2, x3', instr.Add)
        self.verify_mnemonic('sub', 'x1, x2, x3', instr.Sub)
        self.verify_mnemonic('sll', 'x1, x2, x3', instr.Sll)
        self.verify_mnemonic('slt', 'x1, x2, x3', instr.Slt)
        self.verify_mnemonic('sltu', 'x1, x2, x3', instr.Sltu)
        self.verify_mnemonic('xor', 'x1, x2, x3', instr.Xor)
        self.verify_mnemonic('srl', 'x1, x2, x3', instr.Srl)
        self.verify_mnemonic('sra', 'x1, x2, x3', instr.Sra)
        self.verify_mnemonic('or', 'x1, x2, x3', instr.Or)
        self.verify_mnemonic('and', 'x1, x2, x3', instr.And)

        # I-Type
        self.verify_mnemonic('addi', 'x1, x2, 10', instr.Addi)
        self.verify_mnemonic('slti', 'x1, x2, 10', instr.Slti)
        self.verify_mnemonic('sltiu', 'x1, x2, 10', instr.Sltiu)
        self.verify_mnemonic('xori', 'x1, x2, 10', instr.Xori)
        self.verify_mnemonic('ori', 'x1, x2, 10', instr.Ori)
        self.verify_mnemonic('andi', 'x1, x2, 10', instr.Andi)
        self.verify_mnemonic('slli', 'x1, x2, 1', instr.Slli)
        self.verify_mnemonic('srli', 'x1, x2, 1', instr.Srli)
        self.verify_mnemonic('srai', 'x1, x2, 1', instr.Srai)
        
        # Load
        self.verify_mnemonic('lb', 'x1, 0(x2)', instr.Lb)
        self.verify_mnemonic('lh', 'x1, 0(x2)', instr.Lh)
        self.verify_mnemonic('lw', 'x1, 0(x2)', instr.Lw)
        self.verify_mnemonic('lbu', 'x1, 0(x2)', instr.Lbu)
        self.verify_mnemonic('lhu', 'x1, 0(x2)', instr.Lhu)

        # S-Type
        self.verify_mnemonic('sb', 'x1, 0(x2)', instr.Sb)
        self.verify_mnemonic('sh', 'x1, 0(x2)', instr.Sh)
        self.verify_mnemonic('sw', 'x1, 0(x2)', instr.Sw)

        # B-Type
        self.verify_mnemonic('beq', 'x1, x2, 4', instr.Beq)
        self.verify_mnemonic('bne', 'x1, x2, 4', instr.Bne)
        self.verify_mnemonic('blt', 'x1, x2, 4', instr.Blt)
        self.verify_mnemonic('bge', 'x1, x2, 4', instr.Bge)
        self.verify_mnemonic('bltu', 'x1, x2, 4', instr.Bltu)
        self.verify_mnemonic('bgeu', 'x1, x2, 4', instr.Bgeu)

        # U-Type
        self.verify_mnemonic('lui', 'x1, 0x1000', instr.Lui)
        self.verify_mnemonic('auipc', 'x1, 0x1000', instr.Auipc)

        # J-Type
        self.verify_mnemonic('jal', 'x1, 16', instr.Jal)
        self.verify_mnemonic('jalr', 'x1, x2, 0', instr.Jalr)

        # System
        self.verify_mnemonic('fence', '', instr.Fence)
        self.verify_mnemonic('ecall', '', instr.Ecall)
        self.verify_mnemonic('ebreak', '', instr.Ebreak)

if __name__ == '__main__':
    unittest.main()
