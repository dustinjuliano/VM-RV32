"""
Unit tests for the Memory model of the RISC-V emulator.
Focuses on soundness, little-endianness, and bounds checking.
"""

import unittest
from memory import Memory

class TestMemory(unittest.TestCase):
  def setUp(self):
    self.mem = Memory(size=1024)

  def test_basic_byte_rw(self):
    # Test writing and reading individual bytes
    self.assertTrue(self.mem.write_byte(10, 0xAB))
    self.assertEqual(self.mem.read_byte(10), 0xAB)
    self.assertEqual(self.mem.read_byte(11), 0x00)

  def test_little_endian_32bit(self):
    # Test 32-bit word write (0x12345678)
    # Byte 0: 0x78, Byte 1: 0x56, Byte 2: 0x34, Byte 3: 0x12
    self.assertTrue(self.mem.write(100, 4, 0x12345678))
    self.assertEqual(self.mem.read_byte(100), 0x78)
    self.assertEqual(self.mem.read_byte(101), 0x56)
    self.assertEqual(self.mem.read_byte(102), 0x34)
    self.assertEqual(self.mem.read_byte(103), 0x12)
    self.assertEqual(self.mem.read(100, 4), 0x12345678)

  def test_little_endian_16bit(self):
    # Test 16-bit word write (0xABCD)
    # Byte 0: 0xCD, Byte 1: 0xAB
    self.assertTrue(self.mem.write(200, 2, 0xABCD))
    self.assertEqual(self.mem.read_byte(200), 0xCD)
    self.assertEqual(self.mem.read_byte(201), 0xAB)
    self.assertEqual(self.mem.read(200, 2), 0xABCD)

  def test_signed_reads(self):
    # Test signed read of 0xFF (should be -1 as i8, 255 as u8)
    self.mem.write_byte(300, 0xFF)
    self.assertEqual(self.mem.read(300, 1, signed=True), -1)
    self.assertEqual(self.mem.read(300, 1, signed=False), 255)
    
    # Test signed read of 0xFFFF (should be -1 as i16)
    self.mem.write(310, 2, 0xFFFF)
    self.assertEqual(self.mem.read(310, 2, signed=True), -1)
    
    # Test signed read of 0x8000 (should be -32768 as i16)
    self.mem.write(320, 2, 0x8000)
    self.assertEqual(self.mem.read(320, 2, signed=True), -32768)

  def test_bounds_checking(self):
    # Test writing out of bounds
    self.assertFalse(self.mem.write_byte(-1, 0x00))
    self.assertFalse(self.mem.write_byte(1024, 0x00))
    self.assertFalse(self.mem.write(1021, 4, 0x00)) # Crosses boundary
    
    # Test reading out of bounds
    self.assertEqual(self.mem.read_byte(-1), 0)
    self.assertEqual(self.mem.read_byte(1024), 0)
    self.assertIsNone(self.mem.read(1021, 4))

  def test_typed_access(self):
    # Test read_typed and write_typed
    self.mem.write_typed(400, "i32", -123)
    self.assertEqual(self.mem.read_typed(400, "i32"), -123)
    self.assertEqual(self.mem.read_typed(400, "u32"), 0xFFFFFF85) # -123 & 0xFFFFFFFF
    
    self.mem.write_typed(410, "u16", 0x4567)
    self.assertEqual(self.mem.read_typed(410, "u16"), 0x4567)
    
    self.mem.write_typed(420, "i8", -1)
    self.assertEqual(self.mem.read_typed(420, "i8"), -1)
    self.assertEqual(self.mem.read_typed(420, "u8"), 255)

  def test_unsupported_type(self):
    with self.assertRaises(ValueError):
      self.mem.read_typed(0, "u64")
    with self.assertRaises(ValueError):
      self.mem.write_typed(0, "u64", 0)

  def test_little_endian_stress(self):
    # Write a word, read as bytes/halfwords, write halfwords/bytes, read as word
    # 0x11223344 -> Byte 0: 44, 1: 33, 2: 22, 3: 11
    self.mem.write(10, 4, 0x11223344)
    self.assertEqual(self.mem.read(10, 1), 0x44)
    self.assertEqual(self.mem.read(11, 2), 0x2233)
    self.assertEqual(self.mem.read(13, 1), 0x11)

    # Overwrite part
    # 0x10 is 44. Let's change 33 (at 0x11) and 22 (at 0x12) to 0xAAAA
    # Memory: 44 AA AA 11
    self.mem.write(11, 2, 0xAAAA)
    self.assertEqual(self.mem.read(10, 4), 0x11AAAA44)

if __name__ == '__main__':
  unittest.main()
