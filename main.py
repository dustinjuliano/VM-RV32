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
    instruction_map = asm_parser.parse_program(source_code)
  except Exception as e:
    print(f"Error parsing program: {e}")
    sys.exit(1)

  # Initialize the CPU.
  cpu = CPU()
  
  # Execution loop.
  print(f"--- Starting Execution: {args.source} ---")
  try:
    while not cpu.halted:
      cpu.step(instruction_map)
      
      # If PC goes beyond instruction map and no jump occurred, we stop.
      if cpu.pc not in instruction_map and not cpu.halted:
        print(f"--- Execution Finished (PC=0x{cpu.pc:08X}) ---")
        break
    
    if cpu.halted:
      # If we halted due to an error (stack, memory, etc.), exit 1.
      # Assertions are handled by the try-except block below.
      sys.exit(1)
        
  except AssertionError:
    # Assertion error already printed a message.
    sys.exit(1)
  except Exception as e:
    print(f"Runtime Error: {e}")
    sys.exit(1)

if __name__ == "__main__":
  main()
