import unittest
from parser import Parser

class TestSegments(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_basic_segments(self):
        source = """
        .data
        var1: .word 10
        var2: .word 20
        .text
        main:
            addi x1, x1, 1
        """
        result = self.parser.parse_program(source)
        labels = self.parser.labels
        
        # Check segments
        self.assertEqual(labels['var1'], 0x4000)
        self.assertEqual(labels['var2'], 0x4004)
        self.assertEqual(labels['main'], 0x0000)
        
        # Check data values (little endian)
        self.assertEqual(result['data'][0x4000], 10)
        self.assertEqual(result['data'][0x4001], 0)
        self.assertEqual(result['data'][0x4004], 20)

    def test_string_directive(self):
        source = """
        .data
        s1: .string "ABC"
        """
        result = self.parser.parse_program(source)
        # 'A'=65, 'B'=66, 'C'=67, null=0
        self.assertEqual(result['data'][0x4000], 65)
        self.assertEqual(result['data'][0x4001], 66)
        self.assertEqual(result['data'][0x4002], 67)
        self.assertEqual(result['data'][0x4003], 0)

    def test_segment_collision(self):
        # Create a very long .text segment to trigger collision
        # data_base is at 0x4000 (16384 bytes)
        # 16384 bytes / 4 bytes per instruction = 4096 instructions
        source = ".text\n" + "addi x1, x1, 1\n" * 4097
        with self.assertRaises(ValueError) as cm:
            self.parser.parse_program(source)
        self.assertIn("Segment collision!", str(cm.exception))

    def test_label_resolution_across_segments(self):
        source = """
        .data
        target: .word 0x12345678
        .text
        main:
            lw x1, target
        """
        result = self.parser.parse_program(source)
        instrs = result['instructions']
        self.assertIn(0, instrs)
        self.assertIn(4, instrs)
        self.assertEqual(instrs[0][0].__class__.__name__, 'Auipc')
        self.assertEqual(instrs[4][0].__class__.__name__, 'Lw')
        
if __name__ == '__main__':
    unittest.main()
