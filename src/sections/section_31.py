from dataclasses import dataclass
from typing import List
from utils.binary_reader import BinaryReader
from io import BytesIO
from utils.char_table import CharTable

@dataclass(init=False)
class Section31:
  offsets: List[int]
  location_names: List[str]

  def __init__(self, stream: BytesIO):
    self.offsets = self.parse_text_offsets(stream)
    self.location_names = self.parse_location_names(stream)
  
  def parse_text_offsets(self, stream: BytesIO) -> List[int]:
    offsets: List[int] = []
    while True:
      offset = BinaryReader.read_uint32(stream)
      if offset == 0:
        break
      offsets.append(offset)

    return offsets
    
  def parse_location_names(self, stream: BytesIO) -> List[str]:
    location_names: List[str] = []
    
    for i, offset in enumerate(self.offsets):
        start_offset = offset
        end_offset = self.offsets[i + 1] if i + 1 < len(self.offsets) else len(stream.getbuffer())
        stream.seek(start_offset)
        
        name_bytes = stream.read(end_offset - start_offset)
        
        name = CharTable.getTextFromBytes(name_bytes)
        location_names.append(name)
    
    return location_names