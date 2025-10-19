from dataclasses import dataclass
from typing import List
from utils.binary_reader import BinaryReader
from io import BytesIO

@dataclass
class DrawPoint:
  x: int
  y: int
  magicId: int

@dataclass(init=False)
class Section34:
  draw_points: List[DrawPoint]

  def __init__(self, stream: BytesIO):
    stream.seek(44)
    self.draw_points = self.parse_draw_points(stream)
  
  def parse_draw_points(self, stream: BytesIO) -> List[DrawPoint]:
    draw_points: List[DrawPoint] = []
    while stream.tell() < stream.getbuffer().nbytes:
      x = BinaryReader.read_uint8(stream)
      y = BinaryReader.read_uint8(stream)
      magicId = BinaryReader.read_uint16(stream)
      draw_points.append(DrawPoint(x=x, y=y, magicId=magicId))

    return draw_points