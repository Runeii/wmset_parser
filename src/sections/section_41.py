from dataclasses import dataclass
from typing import List
from utils.binary_reader import BinaryReader
from io import BytesIO
from .textures.tim import TIM

@dataclass(init=False)
class Section41:
  offsets: List[int]

  def __init__(self, stream: BytesIO):
    self.offsets = self.parse_text_offsets(stream)
    self.textures = self.parse_textures(stream, self.offsets)

  
  def parse_text_offsets(self, stream: BytesIO) -> List[int]:
    offsets: List[int] = []
    while True:
      offset = BinaryReader.read_uint32(stream)
      if offset == 0:
        break
      offsets.append(offset)

    return offsets
  
  def parse_textures(self, stream: BytesIO, offsets: List[int]):
    textures: List[TIM] = []
    for i, offset in enumerate(offsets):
      start_offset = offset
      end_offset = offsets[i + 1] if i + 1 < len(offsets) else len(stream.getbuffer())
      chunk_size = end_offset - start_offset
      stream.seek(start_offset)
      texture_bytes = stream.read(chunk_size)
      texture_stream = BytesIO(texture_bytes)
      texture = self.parse_tim(texture_stream, f"Texture_{i}")
      textures.append(texture)

    return textures

  def parse_tim(self, stream: BytesIO, name: str) -> TIM:
    return TIM(stream=stream, name=name)