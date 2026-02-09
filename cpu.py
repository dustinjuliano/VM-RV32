"""
This module provides the CPU class for the RISC-V emulator.
It coordinates the register file and memory, and implements the fetch-decode-execute cycle.
"""

from registers import RegisterFile
from memory import Memory

class CPU:
  """
  Represents the RISC-V CPU state and execution logic.
  """

  def __init__(self, mem_size=65536):
    # The register file (x0-x31).
    self.registers = RegisterFile()
    # The byte-addressable memory.
    self.memory = Memory(size=mem_size)
    # The program counter.
    self.pc = 0
    # Flag to stop execution.
    self.halted = False

    # Stack configuration
    self.stack_base = mem_size
    self.stack_limit = mem_size // 2
    self.registers['sp'] = self.stack_base

  def reset(self):
    # Resets the CPU state.
    mem_size = self.memory.size
    self.registers = RegisterFile()
    self.memory = Memory(size=mem_size)
    self.pc = 0
    self.halted = False
    self.registers['sp'] = self.stack_base

  def step(self, instruction_map):
    # Executes all instructions at current PC.
    # instruction_map is a dict {address: [instruction_objects]}.
    if self.pc not in instruction_map:
      print(f"Error: No instruction at PC=0x{self.pc:08X}")
      self.halted = True
      return

    instructions = instruction_map[self.pc]
    # Default increment is based on number of instructions.
    next_pc = self.pc + (4 * len(instructions))
    jump_pc = None
    
    for instr in instructions:
      result_pc = instr.execute(self)
      if result_pc is not None:
        jump_pc = result_pc
      
      if self.halted:
        break
    
    if jump_pc is not None:
      self.pc = jump_pc
    else:
      self.pc = next_pc

    # Stack Protection (only if instruction used the 'sp' alias)
    if any("use_sp" in getattr(instr, 'tags', set()) for instr in instructions):
      sp_val = self.registers['sp']
      if sp_val < self.stack_limit:
          print(f"Runtime Error: Stack Overflow (sp=0x{sp_val:08X}, limit=0x{self.stack_limit:08X})")
          self.halted = True
      elif sp_val > self.stack_base:
          print(f"Runtime Error: Stack Underflow (sp=0x{sp_val:08X}, base=0x{self.stack_base:08X})")
          self.halted = True
