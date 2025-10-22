from dataclasses import dataclass
from typing import List
from utils.binary_reader import BinaryReader
from io import BytesIO
from .opcodes import OPCODES

@dataclass
class Opcode:
  code: str
  param1: int = 0
  param2: int = 0

@dataclass
class Script:
  opcodes: List[Opcode]

@dataclass
class ScriptEntity:
  scripts: List[Script]

@dataclass(init=False)
class GenericScriptSection:
  offsets: List[int]
  entities: List[ScriptEntity]

  def __init__(self, stream: BytesIO):
    self.offsets = self.parse_script_data_offsets(stream)
    self.entities = self.parse_scripts(stream)

  
  def parse_script_data_offsets(self, stream: BytesIO) -> List[int]:
    offsets: List[int] = []
    while True:
      offset = BinaryReader.read_uint32(stream)
      if offset == 0:
        break
      offsets.append(offset)

    return offsets

  def parse_scripts(self, stream: BytesIO) -> List[ScriptEntity]:
    entities: List[ScriptEntity] = []
    for offset in self.offsets:
      stream.seek(offset)
      script = ScriptEntity(scripts=[])
      current_script = Script(opcodes=[])
      while True:
        opcode = BinaryReader.read_int16(stream)
        if opcode == 0:
          break
        param1 = BinaryReader.read_uint8(stream)
        param2 = BinaryReader.read_uint8(stream)
        if opcode == -255:
          if len(current_script.opcodes) > 0:
            script.scripts.append(current_script)
          current_script = Script(opcodes=[])

        current_script.opcodes.append(Opcode(code=OPCODES.get(opcode, {"opcode": "UNRECOGNISED"})["opcode"], param1=param1, param2=param2))

      entities.append(script)
    
    return entities