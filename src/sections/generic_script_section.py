from dataclasses import dataclass
from typing import List
from utils.binary_reader import BinaryReader
from io import BytesIO

@dataclass
class Opcode:
  code: int
  param: int

@dataclass
class Script:
  opcodes: List[Opcode]

@dataclass(init=False)
class GenericScriptSection:
  offsets: List[int]
  scripts: List[Script]

  def __init__(self, stream: BytesIO):
    self.offsets = self.parse_script_data_offsets(stream)
    self.scripts = self.parse_scripts(stream)

  
  def parse_script_data_offsets(self, stream: BytesIO) -> List[int]:
    offsets: List[int] = []
    while True:
      offset = BinaryReader.read_uint32(stream)
      if offset == 0:
        break
      offsets.append(offset)

    return offsets

  def parse_scripts(self, stream: BytesIO) -> List[Script]:
    scripts: List[Script] = []
    for offset in self.offsets:
      stream.seek(offset)
      script = Script(opcodes=[])
      while True:
        offset = BinaryReader.read_uint16(stream)
        if offset == 0:
          break
        param = BinaryReader.read_uint16(stream)
        script.opcodes.append(Opcode(code=offset, param=param))
      scripts.append(script)
    return scripts