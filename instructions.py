"""
This module defines the instruction classes for the RISC-V emulator.
Each class implements an execute(cpu) method.
"""

class Instruction:
  """Base class for all instructions."""
  def __init__(self):
    self.tags = set()

  def execute(self, cpu):
    raise NotImplementedError("Each instruction must implement execute.")

# --- R-Type ---

class RType(Instruction):
  def __init__(self, rd, rs1, rs2):
    super().__init__()
    self.rd = rd
    self.rs1 = rs1
    self.rs2 = rs2

class Add(RType):
  def execute(self, cpu):
    val = (cpu.registers[self.rs1] + cpu.registers[self.rs2]) & 0xFFFFFFFF
    cpu.registers[self.rd] = val

class Sub(RType):
  def execute(self, cpu):
    val = (cpu.registers[self.rs1] - cpu.registers[self.rs2]) & 0xFFFFFFFF
    cpu.registers[self.rd] = val

class Sll(RType):
  def execute(self, cpu):
    shamt = cpu.registers[self.rs2] & 0x1F
    cpu.registers[self.rd] = (cpu.registers[self.rs1] << shamt) & 0xFFFFFFFF

class Slt(RType):
  def execute(self, cpu):
    # Signed comparison
    v1 = cpu.registers[self.rs1]
    if v1 & 0x80000000: v1 -= 0x100000000
    v2 = cpu.registers[self.rs2]
    if v2 & 0x80000000: v2 -= 0x100000000
    cpu.registers[self.rd] = 1 if v1 < v2 else 0

class Sltu(RType):
  def execute(self, cpu):
    cpu.registers[self.rd] = 1 if cpu.registers[self.rs1] < cpu.registers[self.rs2] else 0

class Xor(RType):
  def execute(self, cpu):
    cpu.registers[self.rd] = cpu.registers[self.rs1] ^ cpu.registers[self.rs2]

class Srl(RType):
  def execute(self, cpu):
    shamt = cpu.registers[self.rs2] & 0x1F
    cpu.registers[self.rd] = (cpu.registers[self.rs1] >> shamt) & 0xFFFFFFFF

class Sra(RType):
  def execute(self, cpu):
    shamt = cpu.registers[self.rs2] & 0x1F
    v1 = cpu.registers[self.rs1]
    if v1 & 0x80000000:
      res = ((v1 | 0xFFFFFFFF00000000) >> shamt) & 0xFFFFFFFF
    else:
      res = (v1 >> shamt) & 0xFFFFFFFF
    cpu.registers[self.rd] = res

class Or(RType):
  def execute(self, cpu):
    cpu.registers[self.rd] = cpu.registers[self.rs1] | cpu.registers[self.rs2]

class And(RType):
  def execute(self, cpu):
    cpu.registers[self.rd] = cpu.registers[self.rs1] & cpu.registers[self.rs2]

# --- I-Type ---

class IType(Instruction):
  def __init__(self, rd, rs1, imm):
    super().__init__()
    self.rd = rd
    self.rs1 = rs1
    # imm is usually 12-bit signed
    self.imm = imm

class Addi(IType):
  def execute(self, cpu):
    imm = self.imm & 0xFFF
    if imm & 0x800: imm -= 0x1000
    cpu.registers[self.rd] = (cpu.registers[self.rs1] + imm) & 0xFFFFFFFF

class Slti(IType):
  def execute(self, cpu):
    v1 = cpu.registers[self.rs1]
    if v1 & 0x80000000: v1 -= 0x100000000
    imm = self.imm & 0xFFF
    if imm & 0x800: imm -= 0x1000
    cpu.registers[self.rd] = 1 if v1 < imm else 0

class Sltiu(IType):
  # For SLTIU, immediate is sign-extended then treated as unsigned.
  def execute(self, cpu):
    imm = self.imm & 0xFFF
    if imm & 0x800: imm = (imm - 0x1000) & 0xFFFFFFFF
    else: imm = imm & 0xFFFFFFFF
    cpu.registers[self.rd] = 1 if cpu.registers[self.rs1] < imm else 0

class Xori(IType):
  def execute(self, cpu):
    imm = self.imm & 0xFFF
    if imm & 0x800: imm -= 0x1000
    cpu.registers[self.rd] = cpu.registers[self.rs1] ^ imm

class Ori(IType):
  def execute(self, cpu):
    imm = self.imm & 0xFFF
    if imm & 0x800: imm -= 0x1000
    cpu.registers[self.rd] = cpu.registers[self.rs1] | imm

class Andi(IType):
  def execute(self, cpu):
    imm = self.imm & 0xFFF
    if imm & 0x800: imm -= 0x1000
    cpu.registers[self.rd] = cpu.registers[self.rs1] & imm

class Slli(IType):
  def execute(self, cpu):
    cpu.registers[self.rd] = (cpu.registers[self.rs1] << (self.imm & 0x1F)) & 0xFFFFFFFF

class Srli(IType):
  def execute(self, cpu):
    cpu.registers[self.rd] = (cpu.registers[self.rs1] >> (self.imm & 0x1F)) & 0xFFFFFFFF

class Srai(IType):
  def execute(self, cpu):
    shamt = self.imm & 0x1F
    v1 = cpu.registers[self.rs1]
    if v1 & 0x80000000:
      res = ((v1 | 0xFFFFFFFF00000000) >> shamt) & 0xFFFFFFFF
    else:
      res = (v1 >> shamt) & 0xFFFFFFFF
    cpu.registers[self.rd] = res

# --- Load ---

class Load(IType):
  pass

class Lw(Load):
  def execute(self, cpu):
    imm = self.imm & 0xFFF
    if imm & 0x800: imm -= 0x1000
    addr = (cpu.registers[self.rs1] + imm) & 0xFFFFFFFF
    val = cpu.memory.read(addr, 4, True)
    if val is None:
      cpu.halted = True
      return
    cpu.registers[self.rd] = val

class Lh(Load):
  def execute(self, cpu):
    imm = self.imm & 0xFFF
    if imm & 0x800: imm -= 0x1000
    addr = (cpu.registers[self.rs1] + imm) & 0xFFFFFFFF
    val = cpu.memory.read(addr, 2, True)
    if val is None:
      cpu.halted = True
      return
    cpu.registers[self.rd] = val

class Lhu(Load):
  def execute(self, cpu):
    imm = self.imm & 0xFFF
    if imm & 0x800: imm -= 0x1000
    addr = (cpu.registers[self.rs1] + imm) & 0xFFFFFFFF
    val = cpu.memory.read(addr, 2, False)
    if val is None:
      cpu.halted = True
      return
    cpu.registers[self.rd] = val

class Lb(Load):
  def execute(self, cpu):
    imm = self.imm & 0xFFF
    if imm & 0x800: imm -= 0x1000
    addr = (cpu.registers[self.rs1] + imm) & 0xFFFFFFFF
    val = cpu.memory.read(addr, 1, True)
    if val is None:
      cpu.halted = True
      return
    cpu.registers[self.rd] = val

class Lbu(Load):
  def execute(self, cpu):
    imm = self.imm & 0xFFF
    if imm & 0x800: imm -= 0x1000
    addr = (cpu.registers[self.rs1] + imm) & 0xFFFFFFFF
    val = cpu.memory.read(addr, 1, False)
    if val is None:
      cpu.halted = True
      return
    cpu.registers[self.rd] = val

# --- S-Type ---

class SType(Instruction):
  def __init__(self, rs1, rs2, imm):
    super().__init__()
    self.rs1 = rs1
    self.rs2 = rs2
    self.imm = imm

class Sw(SType):
  def execute(self, cpu):
    imm = self.imm & 0xFFF
    if imm & 0x800: imm -= 0x1000
    addr = (cpu.registers[self.rs1] + imm) & 0xFFFFFFFF
    if not cpu.memory.write(addr, 4, cpu.registers[self.rs2]):
      cpu.halted = True

class Sh(SType):
  def execute(self, cpu):
    imm = self.imm & 0xFFF
    if imm & 0x800: imm -= 0x1000
    addr = (cpu.registers[self.rs1] + imm) & 0xFFFFFFFF
    if not cpu.memory.write(addr, 2, cpu.registers[self.rs2]):
      cpu.halted = True

class Sb(SType):
  def execute(self, cpu):
    imm = self.imm & 0xFFF
    if imm & 0x800: imm -= 0x1000
    addr = (cpu.registers[self.rs1] + imm) & 0xFFFFFFFF
    if not cpu.memory.write(addr, 1, cpu.registers[self.rs2]):
      cpu.halted = True

# --- B-Type ---

class BType(Instruction):
  def __init__(self, rs1, rs2, imm):
    super().__init__()
    self.rs1 = rs1
    self.rs2 = rs2
    self.imm = imm # Relative offset

class Beq(BType):
  def execute(self, cpu):
    imm = self.imm & 0xFFF
    if imm & 0x800: imm -= 0x1000
    if cpu.registers[self.rs1] == cpu.registers[self.rs2]:
      return (cpu.pc + imm) & 0xFFFFFFFF

class Bne(BType):
  def execute(self, cpu):
    imm = self.imm & 0xFFF
    if imm & 0x800: imm -= 0x1000
    if cpu.registers[self.rs1] != cpu.registers[self.rs2]:
      return (cpu.pc + imm) & 0xFFFFFFFF

class Blt(BType):
  def execute(self, cpu):
    imm = self.imm & 0xFFF
    if imm & 0x800: imm -= 0x1000
    v1 = cpu.registers[self.rs1]
    if v1 & 0x80000000: v1 -= 0x100000000
    v2 = cpu.registers[self.rs2]
    if v2 & 0x80000000: v2 -= 0x100000000
    if v1 < v2:
      return (cpu.pc + imm) & 0xFFFFFFFF

class Bge(BType):
  def execute(self, cpu):
    imm = self.imm & 0xFFF
    if imm & 0x800: imm -= 0x1000
    v1 = cpu.registers[self.rs1]
    if v1 & 0x80000000: v1 -= 0x100000000
    v2 = cpu.registers[self.rs2]
    if v2 & 0x80000000: v2 -= 0x100000000
    if v1 >= v2:
      return (cpu.pc + imm) & 0xFFFFFFFF

class Bltu(BType):
  def execute(self, cpu):
    imm = self.imm & 0xFFF
    if imm & 0x800: imm -= 0x1000
    if cpu.registers[self.rs1] < cpu.registers[self.rs2]:
      return (cpu.pc + imm) & 0xFFFFFFFF

class Bgeu(BType):
  def execute(self, cpu):
    imm = self.imm & 0xFFF
    if imm & 0x800: imm -= 0x1000
    if cpu.registers[self.rs1] >= cpu.registers[self.rs2]:
      return (cpu.pc + imm) & 0xFFFFFFFF

# --- U-Type ---

class UType(Instruction):
  def __init__(self, rd, imm):
    super().__init__()
    self.rd = rd
    self.imm = imm # 20-bit imm

class Lui(UType):
  def execute(self, cpu):
    imm = self.imm & 0xFFFFF
    cpu.registers[self.rd] = (imm << 12) & 0xFFFFFFFF

class Auipc(UType):
  def execute(self, cpu):
    imm = self.imm & 0xFFFFF
    cpu.registers[self.rd] = (cpu.pc + (imm << 12)) & 0xFFFFFFFF

# --- J-Type ---

class Jal(Instruction):
  def __init__(self, rd, imm):
    super().__init__()
    self.rd = rd
    self.imm = imm

  def execute(self, cpu):
    imm = self.imm & 0xFFFFF # 20-bit
    if imm & 0x80000: imm -= 0x100000
    cpu.registers[self.rd] = (cpu.pc + 4) & 0xFFFFFFFF
    return (cpu.pc + imm) & 0xFFFFFFFF

class Jalr(Instruction):
  def __init__(self, rd, rs1, imm):
    super().__init__()
    self.rd = rd
    self.rs1 = rs1
    self.imm = imm

  def execute(self, cpu):
    imm = self.imm & 0xFFF
    if imm & 0x800: imm -= 0x1000
    target = (cpu.registers[self.rs1] + imm) & 0xFFFFFFFE
    cpu.registers[self.rd] = (cpu.pc + 4) & 0xFFFFFFFF
    return target

# --- Meta Instructions ---

class Print(Instruction):
  def __init__(self, reg_name, reg_index):
    super().__init__()
    self.reg_name = reg_name
    self.reg_index = reg_index

  def execute(self, cpu):
    if self.reg_index == 'pc':
      val = cpu.pc
    else:
      val = cpu.registers[self.reg_index]
    print(f"[DEBUG] {self.reg_name} = {val} (0x{val:08X})")

class PrintExpression(Instruction):
  def __init__(self, expr_obj, expr_str):
    super().__init__()
    self.expr_obj = expr_obj
    self.expr_str = expr_str

  def execute(self, cpu):
    val = self.expr_obj.evaluate(cpu)
    print(f"[DEBUG] {self.expr_str} = {val} (0x{val:08X})")


class PrintMem(Instruction):
  def __init__(self, addr_expr, type_str, n):
    super().__init__()
    self.addr_expr = addr_expr # Could be a constant or expression
    self.type_str = type_str
    self.n = n

  def execute(self, cpu):
    # For now, addr_expr is an int constant or a register
    addr = self.addr_expr
    print(f"[DEBUG] Memory at 0x{addr:08X} ({self.type_str} x {self.n}):")
    for i in range(self.n):
      val = cpu.memory.read_typed(addr, self.type_str)
      print(f"  0x{addr:08X}: {val}")
      # Increment addr by size of type
      size = {'8': 1, '16': 2, '32': 4}[self.type_str[1:]]
      addr += size

class Assert(Instruction):
  def __init__(self, expression_tree, line_text):
    super().__init__()
    self.expression_tree = expression_tree
    self.line_text = line_text

  def execute(self, cpu):
    # expression_tree should have an evaluate(cpu) method.
    result = self.expression_tree.evaluate(cpu)
    if not result:
      print(f"[ASSERTION FAILED] {self.line_text}")
      cpu.halted = True
      raise AssertionError(f"Assertion failed: {self.line_text}")

# --- System ---

class System(Instruction):
  pass

class Fence(System):
  def execute(self, cpu):
    pass

class Ecall(System):
  def execute(self, cpu):
    print(f"[System] ECALL triggered at PC=0x{cpu.pc:08X}")
    cpu.halted = True

class Ebreak(System):
  def execute(self, cpu):
    print(f"[System] EBREAK triggered at PC=0x{cpu.pc:08X}")
    cpu.halted = True
