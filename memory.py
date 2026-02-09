"""
This module provides the Memory class for the RISC-V emulator.
It implements byte-addressable memory with support for various data types.
"""

import struct

class Memory:
  """
  A byte-addressable memory model using a pre-allocated list.
  Default size is 64KB. Includes bounds checking.
  """

  def __init__(self, size=65536):
    self.size = size
    self._data = [0] * size

  def _check_bounds(self, addr, size):
    # Returns True if access is valid, False otherwise.
    if addr < 0 or (addr + size) > self.size:
      return False
    return True

  def write_byte(self, addr, value):
    # Writes a single byte to memory with bounds checking.
    if not self._check_bounds(addr, 1):
      print(f"Memory Error: Write out of bounds at 0x{addr:08X}")
      return False
    self._data[addr] = value & 0xFF
    return True

  def read_byte(self, addr):
    # Reads a single byte from memory with bounds checking.
    if not self._check_bounds(addr, 1):
      print(f"Memory Error: Read out of bounds at 0x{addr:08X}")
      return 0
    return self._data[addr]

  def write(self, addr, size, value):
    # Writes multiple bytes in little-endian format.
    if not self._check_bounds(addr, size):
      print(f"Memory Error: Write out of bounds at 0x{addr:08X} (size {size})")
      return False
    for i in range(size):
      self._data[addr + i] = (value >> (i * 8)) & 0xFF
    return True

  def read(self, addr, size, signed=False):
    # Reads multiple bytes in little-endian format.
    if not self._check_bounds(addr, size):
      print(f"Memory Error: Read out of bounds at 0x{addr:08X} (size {size})")
      return None
    
    value = 0
    for i in range(size):
      value |= self._data[addr + i] << (i * 8)
    
    if signed:
      bits = size * 8
      if value & (1 << (bits - 1)):
        value -= 1 << bits
    
    return value

  def read_typed(self, addr, type_str):
    # Reads a value based on a type string.
    size_map = {'8': 1, '16': 2, '32': 4}
    size_key = type_str[1:] if type_str[0] in 'ui' else type_str
    if size_key not in size_map:
      raise ValueError(f"Unsupported memory type size: {type_str}")
    
    signed = type_str.startswith('i')
    size = size_map[size_key]
    return self.read(addr, size, signed)

  def write_typed(self, addr, type_str, value):
    # Writes a value based on a type string.
    size_map = {'8': 1, '16': 2, '32': 4}
    size_key = type_str[1:] if type_str[0] in 'ui' else type_str
    if size_key not in size_map:
      raise ValueError(f"Unsupported memory type size: {type_str}")
    
    size = size_map[size_key]
    return self.write(addr, size, value)
