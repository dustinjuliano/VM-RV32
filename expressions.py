"""
This module defines the expression classes for the functional assertion language.
Each class implements an evaluate(cpu) method.
"""

class Expression:
  """Base class for all expressions."""
  def evaluate(self, cpu):
    raise NotImplementedError()

class Literal(Expression):
  def __init__(self, value):
    # Ensure literals are treated as 32-bit values.
    self.value = value & 0xFFFFFFFF
  def evaluate(self, cpu):
    return self.value

class RegAccess(Expression):
  def __init__(self, reg_index):
    self.reg_index = reg_index
  def evaluate(self, cpu):
    return cpu.registers[self.reg_index]

class PCAccess(Expression):
  def evaluate(self, cpu):
    return cpu.pc

class MemAccess(Expression):
  def __init__(self, addr_expr, type_str):
    self.addr_expr = addr_expr # Can be Expression
    self.type_str = type_str
  def evaluate(self, cpu):
    addr = self.addr_expr.evaluate(cpu)
    return cpu.memory.read_typed(addr, self.type_str)

class BinaryOp(Expression):
  def __init__(self, left, right):
    self.left = left
    self.right = right

class Eq(BinaryOp):
  def evaluate(self, cpu):
    return self.left.evaluate(cpu) == self.right.evaluate(cpu)

class Ne(BinaryOp):
  def evaluate(self, cpu):
    return self.left.evaluate(cpu) != self.right.evaluate(cpu)

class Lt(BinaryOp):
  def evaluate(self, cpu):
    return self.left.evaluate(cpu) < self.right.evaluate(cpu)

class Gt(BinaryOp):
  def evaluate(self, cpu):
    return self.left.evaluate(cpu) > self.right.evaluate(cpu)

class Le(BinaryOp):
  def evaluate(self, cpu):
    return self.left.evaluate(cpu) <= self.right.evaluate(cpu)

class Ge(BinaryOp):
  def evaluate(self, cpu):
    return self.left.evaluate(cpu) >= self.right.evaluate(cpu)

class AndExpr(BinaryOp):
  def evaluate(self, cpu):
    return self.left.evaluate(cpu) and self.right.evaluate(cpu)

class OrExpr(BinaryOp):
  def evaluate(self, cpu):
    return self.left.evaluate(cpu) or self.right.evaluate(cpu)

class NotExpr(Expression):
  def __init__(self, inner):
    self.inner = inner
  def evaluate(self, cpu):
    return not self.inner.evaluate(cpu)
