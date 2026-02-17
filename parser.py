"""
This module implements the Parser for the RISC-V assembly emulator.
It handles labels, instructions, and meta-syntax assertions.
"""

import re
import instructions as instr
import expressions as expr

class Parser:
  """
  Parses RISC-V 32I assembly code into executable objects.
  """

  REGISTER_MAP = {f"x{i}": i for i in range(32)}
  # Add some common aliases
  REGISTER_MAP.update({
    "zero": 0, "ra": 1, "sp": 2, "gp": 3, "tp": 4,
    "t0": 5, "t1": 6, "t2": 7, "s0": 8, "fp": 8, "s1": 9,
    "a0": 10, "a1": 11, "a2": 12, "a3": 13, "a4": 14, "a5": 15, "a6": 16, "a7": 17,
    "s2": 18, "s3": 19, "s4": 20, "s5": 21, "s6": 22, "s7": 23, "s8": 24, "s9": 25, "s10": 26, "s11": 27,
    "t3": 28, "t4": 29, "t5": 30, "t6": 31
  })

  def __init__(self):
    self.labels = {}
    self.instructions = {} 
    self.data_memory = {} # addr -> byte
    self.text_base = 0x0000
    self.data_base = 0x4000

  def parse_program(self, source):
    self.labels = {}
    self.instructions = {} 
    self.data_memory = {}
    
    lines = source.splitlines()
    text_addr = self.text_base
    data_addr = self.data_base
    current_segment = '.text'
    
    clean_lines = []

    # First pass: identify labels, advance addresses, and store data
    for line_idx, line in enumerate(lines):
      raw_line = line
      line = line.split('#')[0].strip()
      if not line: continue

      # 1. Handle labels (multiple labels possible on one line)
      while True:
        match = re.match(r'^([a-zA-Z_.]\w*):(.*)', line)
        if match:
          label = match.group(1)
          self.labels[label] = text_addr if current_segment == '.text' else data_addr
          line = match.group(2).strip()
        else: break
      
      if not line: continue

      # 2. Handle directives
      if line.startswith('.'):
        parts = re.split(r'\s+', line)
        directive = parts[0].lower()
        if directive == '.text':
          current_segment = '.text'
          continue
        elif directive == '.data':
          current_segment = '.data'
          continue
        elif directive == '.word':
          if current_segment != '.data':
            raise ValueError(f"Line {line_idx+1}: .word outside .data segment")
          for val_str in re.split(r'[\s,]+', " ".join(parts[1:])):
            if not val_str: continue
            val = int(val_str, 0)
            for i in range(4):
              self.data_memory[data_addr + i] = (val >> (i * 8)) & 0xFF
            data_addr += 4
          continue
        elif directive == '.string':
          if current_segment != '.data':
            raise ValueError(f"Line {line_idx+1}: .string outside .data segment")
          # Handle quoted string
          match = re.search(r'"(.*)"', line)
          if match:
            s = match.group(1).encode().decode('unicode_escape')
            for char in s:
              self.data_memory[data_addr] = ord(char)
              data_addr += 1
            self.data_memory[data_addr] = 0 # Null terminator
            data_addr += 1
          continue

      # 3. Handle instructions (only in .text segment)
      if current_segment == '.text':
          # Collision Safeguard
          if text_addr >= self.data_base:
            raise ValueError(f"Line {line_idx+1}: Segment collision! .text overflowed into .data at 0x{text_addr:08X}")
            
          clean_lines.append((text_addr, line))
          
          # Determine expansion size
          parts = re.split(r'[\s,()]+', line)
          parts = [p for p in parts if p]
          mnemonic = parts[0].lower()
          
          expected = 4
          if mnemonic == 'li' and len(parts) >= 3:
            try:
              imm = int(parts[-1], 0)
              if not (-2048 <= imm <= 2047): expected = 8
            except: expected = 8
          elif mnemonic == 'la' and len(parts) >= 3:
            expected = 8
          elif mnemonic == 'call' and len(parts) >= 2:
            expected = 8
          elif mnemonic == 'lw' and len(parts) == 3 and parts[2] in self.labels:
            # Check if it was a pseudo-lw (PC-relative)
            expected = 8
          
          text_addr += expected
      else:
          # Instructions in .data segment are ignored or could be an error
          pass

    # Second pass: parse instructions
    current_addr = self.text_base
    for addr, line in clean_lines:
      # Pad any gaps from labels/pseudo logic
      while current_addr < addr:
        if current_addr not in self.instructions: 
          self.instructions[current_addr] = [instr.Addi(0, 0, 0)]
        current_addr += 4

      objs = self.parse_line(line, addr)
      if objs:
        if not isinstance(objs, list): objs = [objs]
        for i, obj in enumerate(objs):
            self.instructions[addr + i*4] = [obj]
      
      # Correctly advance current_addr based on what we actually produced
      current_addr = addr + (4 * (len(objs) if isinstance(objs, list) else 1))
    
    return {
        'instructions': self.instructions,
        'data': self.data_memory,
        'start_addr': self.labels.get('main', self.text_base)
    }

  def _parse_line_logic(self, line, addr):
    line = line.strip()
    if line.startswith('@'): return self.parse_meta(line)
    
    parts = re.split(r'[\s,()]+', line)
    parts = [p for p in parts if p]
    mnemonic = parts[0].lower()
    args = parts[1:]

    def get_reg(name):
      if name.lower() not in self.REGISTER_MAP:
        raise ValueError(f"Unknown register: {name}")
      return self.REGISTER_MAP[name.lower()]

    def get_imm(val):
      try:
        return int(val, 0)
      except:
        if val in self.labels: return self.labels[val]
        raise ValueError(f"Invalid immediate or label: {val}")

    def get_rel(val):
      if val in self.labels: return self.labels[val] - addr
      return get_imm(val)

    # --- Pseudos ---
    if mnemonic == 'li':
      rd, imm = get_reg(args[0]), get_imm(args[1])
      if -2048 <= imm <= 2047: return instr.Addi(rd, 0, imm)
      upper = (imm + 0x800) >> 12
      lower = imm & 0xFFF
      if lower & 0x800: lower -= 0x1000
      return [instr.Lui(rd, upper), instr.Addi(rd, rd, lower)]
    
    if mnemonic == 'la':
        rd = get_reg(args[0])
        target = get_imm(args[1])
        diff = target - addr
        hi = (diff + 0x800) >> 12
        lo = diff - (hi << 12)
        return [instr.Auipc(rd, hi), instr.Addi(rd, rd, lo)]
    
    if mnemonic == 'lw' and len(args) == 2 and args[1] in self.labels:
        rd = get_reg(args[0])
        target = self.labels[args[1]]
        diff = target - addr
        hi = (diff + 0x800) >> 12
        lo = diff - (hi << 12)
        return [instr.Auipc(rd, hi), instr.Lw(rd, rd, lo)]
    
    if mnemonic == 'mv': return instr.Addi(get_reg(args[0]), get_reg(args[1]), 0)
    if mnemonic == 'neg': return instr.Sub(get_reg(args[0]), 0, get_reg(args[1]))
    if mnemonic == 'not': return instr.Xori(get_reg(args[0]), get_reg(args[1]), -1)
    if mnemonic == 'nop': return instr.Addi(0, 0, 0)
    if mnemonic == 'j': return instr.Jal(0, get_rel(args[0]))
    if mnemonic == 'jr': return instr.Jalr(0, get_reg(args[0]), 0)
    if mnemonic == 'ret': return instr.Jalr(0, 1, 0)
    if mnemonic == 'call':
        target = get_imm(args[0])
        return [instr.Auipc(1, 0), instr.Jalr(1, 1, target - addr)]

    # Zero-based branches/sets
    if mnemonic == 'seqz': return instr.Sltiu(get_reg(args[0]), get_reg(args[1]), 1)
    if mnemonic == 'snez': return instr.Sltu(get_reg(args[0]), 0, get_reg(args[1]))
    if mnemonic == 'sltz': return instr.Slt(get_reg(args[0]), get_reg(args[1]), 0)
    if mnemonic == 'sgtz': return instr.Slt(get_reg(args[0]), 0, get_reg(args[1]))
    
    if mnemonic == 'beqz': return instr.Beq(get_reg(args[0]), 0, get_rel(args[1]))
    if mnemonic == 'bnez': return instr.Bne(get_reg(args[0]), 0, get_rel(args[1]))
    if mnemonic == 'blez': return instr.Bge(0, get_reg(args[0]), get_rel(args[1]))
    if mnemonic == 'bgez': return instr.Bge(get_reg(args[0]), 0, get_rel(args[1]))
    if mnemonic == 'bltz': return instr.Blt(get_reg(args[0]), 0, get_rel(args[1]))
    if mnemonic == 'bgtz': return instr.Blt(0, get_reg(args[0]), get_rel(args[1]))

    if mnemonic == 'fence': return instr.Fence()
    if mnemonic == 'ecall': return instr.Ecall()
    if mnemonic == 'ebreak': return instr.Ebreak()

    # --- Base ---
    if mnemonic in ['add', 'sub', 'sll', 'slt', 'sltu', 'xor', 'srl', 'sra', 'or', 'and', 'mul']:
      return getattr(instr, mnemonic.capitalize())(get_reg(args[0]), get_reg(args[1]), get_reg(args[2]))
    if mnemonic in ['addi', 'slti', 'sltiu', 'xori', 'ori', 'andi', 'slli', 'srli', 'srai']:
      return getattr(instr, mnemonic.capitalize())(get_reg(args[0]), get_reg(args[1]), get_imm(args[2]))
    if mnemonic in ['lw', 'lh', 'lhu', 'lb', 'lbu']:
      return getattr(instr, mnemonic.capitalize())(get_reg(args[0]), get_reg(args[2]), get_imm(args[1]))
    if mnemonic in ['sw', 'sh', 'sb']:
      return getattr(instr, mnemonic.capitalize())(get_reg(args[2]), get_reg(args[0]), get_imm(args[1]))
    if mnemonic in ['beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu', 'bgt', 'ble', 'bgtu', 'bleu']:
      m_base = mnemonic
      if mnemonic == 'bgt': return instr.Blt(get_reg(args[1]), get_reg(args[0]), get_rel(args[2]))
      if mnemonic == 'ble': return instr.Bge(get_reg(args[1]), get_reg(args[0]), get_rel(args[2]))
      if mnemonic == 'bgtu': return instr.Bltu(get_reg(args[1]), get_reg(args[0]), get_rel(args[2]))
      if mnemonic == 'bleu': return instr.Bgeu(get_reg(args[1]), get_reg(args[0]), get_rel(args[2]))
      return getattr(instr, mnemonic.capitalize())(get_reg(args[0]), get_reg(args[1]), get_rel(args[2]))
    if mnemonic in ['lui', 'auipc']:
      return getattr(instr, mnemonic.capitalize())(get_reg(args[0]), get_imm(args[1]))
    if mnemonic == 'jal':
      if len(args) == 1: return instr.Jal(1, get_rel(args[0]))
      return instr.Jal(get_reg(args[0]), get_rel(args[1]))
    if mnemonic == 'jalr':
      # Handle both formats: jalr rd, rs1, imm AND jalr rd, imm(rs1)
      try: return instr.Jalr(get_reg(args[0]), get_reg(args[2]), get_imm(args[1]))
      except: return instr.Jalr(get_reg(args[0]), get_reg(args[1]), get_imm(args[2]))
    
    raise ValueError(f"Unknown mnemonic: {mnemonic}")

  def parse_meta(self, line):
    if line.startswith('@print '):
      name = line[7:].strip()
      # Try known register/pc first
      if name.lower() == 'pc': return instr.Print('PC', 'pc')
      if name.lower() in self.REGISTER_MAP: return instr.Print(name, self.REGISTER_MAP[name.lower()])
      # If not a simple register, try parsing as expression
      try:
        expr_obj = self.parse_expr(name)
        return instr.PrintExpression(expr_obj, name)
      except:
        return instr.Print(name, self.REGISTER_MAP[name.lower()]) # Fallback to trigger original error if needed

    if line.startswith('@print_mem '):
      p = line[11:].split()
      return instr.PrintMem(int(p[0], 0), p[1], int(p[2]) if len(p) > 2 else 1)
    if line.startswith('@assert '):
      expr_str = line[8:].strip()
      return instr.Assert(self.parse_expr(expr_str), expr_str)
    return None

  def parse_expr(self, expr_str):
    tokens = re.findall(r'[a-zA-Z_]\w*|0x[0-9a-fA-F]+|0b[01]+|-?\d+|[(),\[\]]', expr_str)
    self._expr_pos = 0
    def parse_next():
      token = tokens[self._expr_pos]
      self._expr_pos += 1
      if token == 'm' and tokens[self._expr_pos] == '[':
        self._expr_pos += 1
        a = parse_next()
        self._expr_pos += 1 # ,
        t = tokens[self._expr_pos]; self._expr_pos += 1
        self._expr_pos += 1 # ]
        return expr.MemAccess(a, t)
      if token.lower() == 'pc': return expr.PCAccess()
      if token.lower() in self.REGISTER_MAP: return expr.RegAccess(self.REGISTER_MAP[token.lower()])
      if re.match(r'^-?\d+|0x[0-9a-fA-F]+', token): return expr.Literal(int(token, 0))
      if self._expr_pos < len(tokens) and tokens[self._expr_pos] == '(':
        self._expr_pos += 1
        args = []
        while tokens[self._expr_pos] != ')':
          args.append(parse_next())
          if tokens[self._expr_pos] == ',': self._expr_pos += 1
        self._expr_pos += 1
        name = token.lower()
        if name == 'eq': return expr.Eq(args[0], args[1])
        if name == 'ne': return expr.Ne(args[0], args[1])
        if name == 'lt': return expr.Lt(args[0], args[1])
        if name == 'gt': return expr.Gt(args[0], args[1])
        if name == 'le': return expr.Le(args[0], args[1])
        if name == 'ge': return expr.Ge(args[0], args[1])
        if name == 'and': return expr.AndExpr(args[0], args[1])
        if name == 'or': return expr.OrExpr(args[0], args[1])
        if name == 'and': return expr.AndExpr(args[0], args[1])
        if name == 'or': return expr.OrExpr(args[0], args[1])
        if name == 'not': return expr.NotExpr(args[0])
        if name == 'add': return expr.Add(args[0], args[1])
        if name == 'sub': return expr.Sub(args[0], args[1])
        if name == 'mul': return expr.Mul(args[0], args[1])
        if name == 'div': return expr.Div(args[0], args[1])
        if name == 'mod': return expr.Mod(args[0], args[1])

      raise ValueError(f"Unexpected token: {token}")
    return parse_next()

  def parse_line(self, line, addr):
    # Wrapper to auto-tag instructions that use 'sp'
    objs = self._parse_line_logic(line, addr)
    if objs:
        parts = re.split(r'[\s,()]+', line)
        if 'sp' in parts:
            iterator = objs if isinstance(objs, list) else [objs]
            for obj in iterator:
                obj.tags.add("use_sp")
    return objs
