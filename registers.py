"""
This module provides the RegisterFile class for the RISC-V emulator.
It manages 32 general-purpose 32-bit registers.
"""

class RegisterFile:
  """
  Manages the 32 general-purpose registers (x0-x31).
  Register x0 is hardwired to zero.
  """

  ALIAS_MAP = {
    "zero": 0, "ra": 1, "sp": 2, "gp": 3, "tp": 4,
    "t0": 5, "t1": 6, "t2": 7, "s0": 8, "fp": 8, "s1": 9,
    "a0": 10, "a1": 11, "a2": 12, "a3": 13, "a4": 14, "a5": 15, "a6": 16, "a7": 17,
    "s2": 18, "s3": 19, "s4": 20, "s5": 21, "s6": 22, "s7": 23, "s8": 24, "s9": 25, "s10": 26, "s11": 27,
    "t3": 28, "t4": 29, "t5": 30, "t6": 31
  }

  def __init__(self):
    # Initialize 32 registers to 0.
    self._regs = [0] * 32

  def _resolve(self, key):
    # Resolves a key (index or alias) to a valid register index (0-31).
    if isinstance(key, str):
      name = key.lower().lstrip('x')
      if name.isdigit():
        idx = int(name)
      elif name in self.ALIAS_MAP:
        idx = self.ALIAS_MAP[name]
      else:
        raise ValueError(f"Unknown register alias: {key}")
    else:
      idx = key
    
    if not (0 <= idx < 32):
      raise IndexError(f"Register index out of range: {idx}")
    return idx

  def read(self, key):
    # Reads the value of a register. x0 always returns 0.
    idx = self._resolve(key)
    if idx == 0:
      return 0
    return self._regs[idx] & 0xFFFFFFFF

  def write(self, key, value):
    # Writes a value to a register. x0 remains 0.
    idx = self._resolve(key)
    if idx == 0:
      return
    self._regs[idx] = value & 0xFFFFFFFF

  def __getitem__(self, key):
    # Allows array-style access: rf[0].
    return self.read(key)

  def __setitem__(self, key, value):
    # Allows array-style assignment: rf[1] = 10.
    self.write(key, value)
