import unittest
import json
import os
import sys
import re

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import instructions as instr
from parser import Parser

class TestTraceability(unittest.TestCase):
    def setUp(self):
        matrix_path = os.path.join(os.path.dirname(__file__), "..", "doc", "compliance_matrix.json")
        with open(matrix_path, "r") as f:
            self.matrix = json.load(f)

    def test_matrix_to_code_parity(self):
        """Verify all classes in matrix exist in instructions.py."""
        # 1. Check direct classes
        instruction_classes = []
        for section in self.matrix.values():
            for item in section.values():
                if "class" in item:
                    instruction_classes.append(item["class"])
                if "expansion" in item:
                    instruction_classes.extend(item["expansion"])

        for cls_name in instruction_classes:
            self.assertTrue(hasattr(instr, cls_name), f"Class {cls_name} defined in matrix not found in instructions.py")

    def test_forward_traceability_completeness(self):
        """Verify every instruction class in instructions.py is in the matrix."""
        # Get all subclasses of Instruction that aren't base types
        base_classes = {'Instruction', 'RType', 'IType', 'Load', 'SType', 'BType', 'UType', 'System'}
        implemented_classes = set()
        for name in dir(instr):
            obj = getattr(instr, name)
            if isinstance(obj, type) and issubclass(obj, instr.Instruction) and name not in base_classes:
                implemented_classes.add(name)

        # Collect mapped classes
        mapped_classes = set()
        for section in self.matrix.values():
            for item in section.values():
                if "class" in item:
                    mapped_classes.add(item["class"])
                if "expansion" in item:
                    for c in item["expansion"]:
                        mapped_classes.add(c)

        unmapped = implemented_classes - mapped_classes
        self.assertEqual(unmapped, set(), f"Implemented instruction classes not found in compliance_matrix.json: {unmapped}")

    def test_test_existence(self):
        """Verify all test methods referenced in matrix exist in the tests/ directory."""
        tests_dir = os.path.dirname(__file__)
        for section in self.matrix.values():
            for item in section.values():
                for test_ref in item.get("tests", []):
                    file_name, method_name = test_ref.split(":")
                    file_path = os.path.join(tests_dir, file_name)
                    self.assertTrue(os.path.exists(file_path), f"Test file {file_name} referenced in matrix does not exist")
                    
                    with open(file_path, "r") as f:
                        content = f.read()
                        self.assertIn(method_name, content, f"Test method {method_name} not found in {file_name}")

if __name__ == '__main__':
    unittest.main()
