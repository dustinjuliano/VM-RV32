"""
This is the main entry point for the RISC-V 32I assembly emulator.
It provides a command-line interface to load and execute RISC-V programs.
"""

import sys
import argparse
from cpu import CPU
from parser import Parser

def main():
  # Set up command-line argument parsing.
  parser = argparse.ArgumentParser(description="RISC-V 32I Assembly Emulator")
  parser.add_argument("source", help="The RISC-V assembly file to execute")
  parser.add_argument("--trace", action="store_true", help="Print PC at each step")
  
  args = parser.parse_args()

  # Read the source file.
  try:
    with open(args.source, 'r') as f:
      source_code = f.read()
  except Exception as e:
    print(f"Error reading source file: {e}")
    sys.exit(1)

  # Parse the program.
  asm_parser = Parser()
  try:
    parse_result = asm_parser.parse_program(source_code)
    instruction_map = parse_result['instructions']
    data_map = parse_result['data']
    start_addr = parse_result['start_addr']
  except Exception as e:
    print(f"Error parsing program: {e}")
    sys.exit(1)

  # Initialize the CPU.
  cpu = CPU()
  
  # Reset CPU to start address
  cpu.reset(start_pc=start_addr)

  # Load data into memory
  for addr, val in data_map.items():
    cpu.memory.write_byte(addr, val)
  
  # Execution loop.
  try:
    while not cpu.halted:
      if args.trace:
        print(f"Trace: PC=0x{cpu.pc:08X}")
      
      cpu.step(instruction_map)
      
      # If PC goes beyond instruction map and no jump occurred, we stop.
      if cpu.pc not in instruction_map and not cpu.halted:
        break
    
    if cpu.halted and cpu.registers[17] != 10: # a7=10 is clean exit
      # If we halted due to an error, exit 1.
      # Syscall 10 (Exit) is not an error.
      pass
        
  except AssertionError:
    # Assertion error already printed a message.
    sys.exit(1)
  except Exception as e:
    print(f"Runtime Error: {e}")
    sys.exit(1)

if __name__ == "__main__":
  main()
