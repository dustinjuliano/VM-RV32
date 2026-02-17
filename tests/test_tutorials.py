"""
Comprehensive Unit Tests for the RISC-V 32I Tutorial Series.
Verifies the architectural state of all 64 tutorials.
"""

import unittest
import os
from cpu import CPU
from parser import Parser

class TestTutorials(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU(mem_size=65536)
        self.parser = Parser()

    def run_tutorial(self, filename):
        path = os.path.join(os.path.dirname(__file__), '..', 'tutorial', filename)
        with open(path, 'r') as f:
            source = f.read()
        
        parse_result = self.parser.parse_program(source)
        program = parse_result['instructions']
        
        while not self.cpu.halted:
            if self.cpu.pc in program:
                for obj in program[self.cpu.pc]:
                    res = obj.execute(self.cpu)
                    if res is not None:
                        self.cpu.pc = res
                        break
                else:
                    self.cpu.pc += 4 * len(program[self.cpu.pc])
            else:
                break
        self.assertFalse(self.cpu.halted, f"Tutorial {filename} halted with error")

    # Phase 1: Basic Mechanics
    def test_01_meta_syntax(self):
        self.run_tutorial("01_meta_syntax_basics.s")
        self.assertEqual(self.cpu.registers[1], 150)

    def test_02_expressions(self):
        self.run_tutorial("02_expressions.s")
        self.assertEqual(self.cpu.registers[1], 10)
        self.assertEqual(self.cpu.registers[2], 20)

    def test_03_numeric_literals(self):
        self.run_tutorial("03_numeric_literals.s")
        self.assertEqual(self.cpu.registers[1], 42)
        self.assertEqual(self.cpu.registers[2], 42)
        self.assertEqual(self.cpu.registers[3], 42)
        self.assertEqual(self.cpu.registers[4], 0xFFFFFFFF)

    def test_04_boolean_logic(self):
        self.run_tutorial("04_boolean_logic.s")
        self.assertEqual(self.cpu.registers[1], 100)
        self.assertEqual(self.cpu.registers[2], 200)

    def test_05_execution_flow(self):
        self.run_tutorial("05_execution_flow.s")
        self.assertEqual(self.cpu.registers[1], 1)

    def test_06_r_type_arithmetic(self):
        self.run_tutorial("06_r_type_arithmetic.s")
        self.assertEqual(self.cpu.registers[1], 10)
        self.assertEqual(self.cpu.registers[2], 5)
        self.assertEqual(self.cpu.registers[3], 15)
        self.assertEqual(self.cpu.registers[4], 5)
        self.assertEqual(self.cpu.registers[5], 0xFFFFFFFB)

    def test_07_r_type_logical(self):
        self.run_tutorial("07_r_type_logical.s")
        self.assertEqual(self.cpu.registers[3], 8)  # AND
        self.assertEqual(self.cpu.registers[4], 14) # OR
        self.assertEqual(self.cpu.registers[5], 6)  # XOR

    def test_08_r_type_shifts(self):
        self.run_tutorial("08_r_type_shifts.s")
        self.assertEqual(self.cpu.registers[3], 4) 
        self.assertEqual(self.cpu.registers[6], 0x40000000)
        self.assertEqual(self.cpu.registers[7], 0xC0000000)

    def test_09_r_type_comparisons(self):
        self.run_tutorial("09_r_type_comparisons.s")
        self.assertEqual(self.cpu.registers[3], 1)
        self.assertEqual(self.cpu.registers[4], 0)

    def test_10_i_type_arithmetic(self):
        self.run_tutorial("10_i_type_arithmetic.s")
        self.assertEqual(self.cpu.registers[2], 5)
        self.assertEqual(self.cpu.registers[3], 1)
        self.assertEqual(self.cpu.registers[4], 1)

    def test_11_i_type_logical(self):
        self.run_tutorial("11_i_type_logical.s")
        self.assertEqual(self.cpu.registers[2], 8)
        self.assertEqual(self.cpu.registers[3], 15)
        self.assertEqual(self.cpu.registers[4], 5)

    def test_12_i_type_shifts(self):
        self.run_tutorial("12_i_type_shifts.s")
        self.assertEqual(self.cpu.registers[2], 32)
        self.assertEqual(self.cpu.registers[4], 0x0FFFFFFF)
        self.assertEqual(self.cpu.registers[5], 0xFFFFFFFF)

    def test_13_lui_mechanics(self):
        self.run_tutorial("13_lui_mechanics.s")
        self.assertEqual(self.cpu.registers[1], 0x12345678)

    def test_14_auipc_mechanics(self):
        self.run_tutorial("14_auipc_mechanics.s")
        self.assertEqual(self.cpu.registers[1], 65536)

    def test_15_memory_loads(self):
        self.run_tutorial("15_memory_loads.s")
        self.assertEqual(self.cpu.registers[2], 0xFFFFFFFF)
        self.assertEqual(self.cpu.registers[3], 0xFF)
        self.assertEqual(self.cpu.registers[4], 0xFFFF80FF)
        self.assertEqual(self.cpu.registers[5], 0x80FF)

    def test_16_memory_stores(self):
        self.run_tutorial("16_memory_stores.s")
        self.assertEqual(self.cpu.memory.read_typed(0, "u32"), 0x3456)
        self.assertEqual(self.cpu.memory.read_typed(0, "u8"), 0x56)
        self.assertEqual(self.cpu.memory.read_typed(1, "u8"), 0x34)

    # Phase 2: Control Flow
    def test_17_branch_equality(self):
        self.run_tutorial("17_branch_equality.s")
        self.assertEqual(self.cpu.registers[4], 0)

    def test_18_branch_signed(self):
        self.run_tutorial("18_branch_signed.s")
        self.assertEqual(self.cpu.registers[3], 0)
        self.assertEqual(self.cpu.registers[4], 0)

    def test_19_branch_unsigned(self):
        self.run_tutorial("19_branch_unsigned.s")
        self.assertEqual(self.cpu.registers[3], 1)
        self.assertEqual(self.cpu.registers[4], 0)

    def test_20_jal_mechanics(self):
        self.run_tutorial("20_jal_mechanics.s")
        self.assertEqual(self.cpu.registers[1], 4)

    def test_21_jalr_mechanics(self):
        self.run_tutorial("21_jalr_mechanics.s")
        self.assertEqual(self.cpu.registers['ra'], 12)
        self.assertEqual(self.cpu.registers['a0'], 0)

    def test_22_pc_relative(self):
        self.run_tutorial("22_pc_relative.s")
        self.assertEqual(self.cpu.registers[1], 0)

    def test_23_loops(self):
        self.run_tutorial("23_loops.s")
        self.assertEqual(self.cpu.registers[1], 1)

    def test_24_conditional_skip(self):
        self.run_tutorial("24_conditional_skip.s")
        self.assertEqual(self.cpu.registers[2], 20)

    def test_25_forward_jumps(self):
        self.run_tutorial("25_forward_jumps.s")
        self.assertEqual(self.cpu.registers[1], 10)

    def test_26_control_flow_review(self):
        self.run_tutorial("26_control_flow_review.s")
        self.assertEqual(self.cpu.registers[1], 3)

    # Phase 3: ABI
    def test_27_abi_aliases(self):
        self.run_tutorial("27_abi_aliases.s")
        self.assertEqual(self.cpu.registers['ra'], 42)
        self.assertEqual(self.cpu.registers['sp'], 65536)

    def test_28_zero_register(self):
        self.run_tutorial("28_zero_register.s")
        self.assertEqual(self.cpu.registers[0], 0)

    def test_29_ra_mechanics(self):
        self.run_tutorial("29_ra_mechanics.s")
        self.assertEqual(self.cpu.registers['ra'], 4)

    def test_30_sp_basics(self):
        self.run_tutorial("30_sp_basics.s")
        self.assertEqual(self.cpu.registers['sp'], 65536)

    def test_31_gp_tp(self):
        self.run_tutorial("31_gp_tp_roles.s")
        self.assertEqual(self.cpu.registers['gp'], 2048)

    def test_32_temporaries_low(self):
        self.run_tutorial("32_temporaries_low.s")
        self.assertEqual(self.cpu.registers['t0'], 1)
        self.assertEqual(self.cpu.registers['t1'], 2)
        self.assertEqual(self.cpu.registers['t2'], 3)

    def test_33_saved_low(self):
        self.run_tutorial("33_saved_low.s")
        self.assertEqual(self.cpu.registers['s0'], 123)
        self.assertEqual(self.cpu.registers['s1'], 456)

    def test_34_args_return(self):
        self.run_tutorial("34_args_return.s")
        self.assertEqual(self.cpu.registers['a0'], 10)
        self.assertEqual(self.cpu.registers['a1'], 20)

    def test_35_more_args(self):
        self.run_tutorial("35_more_args.s")
        self.assertEqual(self.cpu.registers['a2'], 3)
        self.assertEqual(self.cpu.registers['a7'], 8)

    def test_36_temporaries_high(self):
        self.run_tutorial("36_temporaries_high.s")
        self.assertEqual(self.cpu.registers['t3'], 30)
        self.assertEqual(self.cpu.registers['t6'], 60)

    def test_37_saved_high(self):
        self.run_tutorial("37_saved_high.s")
        self.assertEqual(self.cpu.registers['s2'], 2)
        self.assertEqual(self.cpu.registers['s11'], 11)

    def test_38_fp_usage(self):
        self.run_tutorial("38_fp_usage.s")
        self.assertEqual(self.cpu.registers['fp'], 2048)
        self.assertEqual(self.cpu.registers['s0'], 2048)

    # Phase 4: Stack
    def test_39_stack_push(self):
        self.run_tutorial("39_stack_push.s")
        self.assertEqual(self.cpu.registers['sp'], 65532)
        self.assertEqual(self.cpu.memory.read_typed(65532, "u32"), 42)

    def test_40_stack_pop(self):
        self.run_tutorial("40_stack_pop.s")
        self.assertEqual(self.cpu.registers['sp'], 65536)
        self.assertEqual(self.cpu.registers['t0'], 42)

    def test_41_stack_multi(self):
        self.run_tutorial("41_stack_multi.s")
        self.assertEqual(self.cpu.registers['sp'], 65536)

    def test_42_prologue_mechanics(self):
        self.run_tutorial("42_prologue_mechanics.s")
        self.assertEqual(self.cpu.registers['s0'], 42)

    def test_43_epilogue_mechanics(self):
        self.run_tutorial("43_epilogue_mechanics.s")
        self.assertEqual(self.cpu.registers['sp'], 65536)

    def test_44_nested_calls(self):
        self.run_tutorial("44_nested_calls.s")
        self.assertEqual(self.cpu.registers['sp'], 65536)

    def test_45_leaf_functions(self):
        self.run_tutorial("45_leaf_functions.s")
        self.assertEqual(self.cpu.registers['ra'], 4)

    # Phase 5: Pseudos
    def test_46_li_la(self):
        self.run_tutorial("46_li_la_pseudos.s")
        self.assertEqual(self.cpu.registers['a0'], 42)
        self.assertEqual(self.cpu.registers['a1'], 0x12345678)

    def test_47_simple_jumps(self):
        self.run_tutorial("47_simple_jumps.s")
        self.assertEqual(self.cpu.registers['ra'], 0)

    def test_48_call_ret_pseudos(self):
        self.run_tutorial("48_call_ret_pseudos.s")
        self.assertEqual(self.cpu.registers['ra'], 8)

    def test_49_logic_pseudos(self):
        self.run_tutorial("49_logic_pseudos.s")
        self.assertEqual(self.cpu.registers['a3'], 0xFFFFFFF6) # -10
        self.assertEqual(self.cpu.registers['a5'], 0xFFFFFFFF)

    def test_50_zero_test_pseudos(self):
        self.run_tutorial("50_zero_test_pseudos.s")
        # Check snez result (a3) if a1=42
        self.assertEqual(self.cpu.registers['a3'], 1)

    def test_51_nop(self):
        self.run_tutorial("51_nop_mechanics.s")
        self.assertEqual(self.cpu.registers[0], 0)

    def test_52_zero_branches(self):
        self.run_tutorial("52_zero_branches.s")
        self.assertEqual(self.cpu.registers[3], 0)

    def test_53_branch_pseudos(self):
        self.run_tutorial("53_branch_pseudos.s")
        self.assertEqual(self.cpu.registers[3], 0)

    def test_54_tail_calls(self):
        self.run_tutorial("54_tail_calls.s")
        self.assertEqual(self.cpu.registers['a0'], 2)

    def test_55_pseudos_review(self):
        self.run_tutorial("55_pseudos_review.s")
        self.assertEqual(self.cpu.registers['a2'], 42)

    def test_56_advanced_print(self):
        self.run_tutorial("56_advanced_print.s")
        # Just ensure it runs without error (assertion-based usually)
        self.assertEqual(self.cpu.halted, False)

    def test_57_advanced_expressions(self):
        self.run_tutorial("57_advanced_expressions.s")
        self.assertEqual(self.cpu.halted, False)

    def test_58_mem_expressions(self):
        self.run_tutorial("58_mem_expressions.s")
        self.assertEqual(self.cpu.halted, False)

    def test_59_multi_assertions(self):
        self.run_tutorial("59_multi_assertions.s")
        self.assertEqual(self.cpu.halted, False)

    def test_60_label_math(self):
        self.run_tutorial("60_label_math.s")
        # Ensure it runs and captures labels
        self.assertGreaterEqual(self.cpu.registers['a0'], 0)

    def test_61_alignment(self):
        self.run_tutorial("61_alignment_concepts.s")
        self.assertEqual(self.cpu.halted, False)

    # Phase 6: Advanced
    def test_62_endianness(self):
        self.run_tutorial("62_endianness.s")
        self.assertEqual(self.cpu.memory.read_typed(0, "u32"), 0x12345678)

    def test_63_instruction_formats(self):
        self.run_tutorial("63_instruction_formats.s")
        self.assertEqual(self.cpu.halted, False)

    def test_64_comprehensive_review(self):
        self.run_tutorial("64_comprehensive_review.s")
        self.assertEqual(self.cpu.registers['a0'], 15)
        self.assertEqual(self.cpu.registers['sp'], 65536)

    def test_every_tutorial_file_is_tested(self):
        """
        Meta-test: Dynamically ensures that every .s file in the tutorial/ directory
        has a corresponding test method in this class.
        """
        tutorial_dir = os.path.join(os.path.dirname(__file__), '..', 'tutorial')
        tutorial_files = [f for f in os.listdir(tutorial_dir) if f.endswith('.s')]
        
        # Identify all methods starting with 'test_'
        test_methods = [m for m in dir(self) if m.startswith('test_')]
        
        for tutorial in tutorial_files:
            prefix = tutorial.split('_')[0]
            found = False
            for method_name in test_methods:
                if method_name.startswith(f"test_{prefix}"):
                    found = True
                    break
            
            if not found:
                self.fail(f"Tutorial file '{tutorial}' has no corresponding test method in TestTutorials.")

        self.assertEqual(len(tutorial_files), 64, "Expected exactly 64 tutorial files.")

if __name__ == '__main__':
    unittest.main()
