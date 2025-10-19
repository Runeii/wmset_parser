from dataclasses import dataclass
from typing import List
from utils.binary_reader import BinaryReader
from io import BytesIO

@dataclass(init=False)
class FileHeader:
  model_count: int
  sections: List[BytesIO]
  offsets: List[int]

  def __init__(self, file_data: bytes):
      if len(file_data) < 0x800:
          print(f"File too short: {len(file_data)} bytes")
          self.model_count = 0
          return None

      stream = BytesIO(file_data)

      self.offsets = self.parse_offsets(stream, 48)
      
      ## Check last offset equals current stream position
      if self.offsets[0] != stream.tell() + 4:
          print(f"Warning: First section offset {self.offsets[0]} does not match stream position {stream.tell()}")

      self.sections = self.parse_sections(stream, self.offsets)
      print(f"Parsed {len(self.sections)} sections from file header")

  def parse_offsets(self, stream: BytesIO, count: int) -> List[int]:
    offsets: List[int] = []
    for _ in range(count):
      offsets.append(BinaryReader.read_uint32(stream))
    
    print("Stream position after header parsing:", stream.tell())
    return offsets

  def parse_sections(self, stream: BytesIO, offsets: List[int]) -> List[BytesIO]:
    sections: List[BytesIO] = []
    for i, offset in enumerate(offsets):
      stream.seek(offset)
      end_offset = offsets[i + 1] if i + 1 < len(offsets) else len(stream.getbuffer())
      section_size = end_offset - offset
      section_data = BinaryReader.read_bytes(stream, section_size)
      sections.append(BytesIO(section_data))
    
    return sections
