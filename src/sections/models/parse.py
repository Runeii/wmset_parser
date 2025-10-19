from dataclasses import dataclass
from typing import List
from io import BytesIO
import struct
from utils.binary_reader import BinaryReader


@dataclass(init=False)
class Triangle:
    data: bytes
    vertex_indices: List[int]
    semitransp: int
    texcoords1: List[int]
    texcoords2: List[int]
    texcoords3: List[int]
    clut_id: int
    
    def __init__(self, data: bytes):
        self.data = data
        stream = BytesIO(self.data)
        self.vertex_indices = [BinaryReader.read_uint8(stream) for _ in range(3)]
        self.semitransp = BinaryReader.read_uint8(stream)
        self.texcoords1 = [BinaryReader.read_uint8(stream) for _ in range(2)]
        self.texcoords2 = [BinaryReader.read_uint8(stream) for _ in range(2)]
        self.texcoords3 = [BinaryReader.read_uint8(stream) for _ in range(2)]
        self.clut_id = BinaryReader.read_uint16(stream)
    
    def __repr__(self):
        return (f"Triangle(vertices={self.vertex_indices}, "
                f"semitransp={bool(self.semitransp & 0x01)}, "
                f"clut_id={self.clut_id})")


@dataclass(init=False)
class Quad:
    data: bytes
    vertex_indices: List[int]
    texcoords1: List[int]
    texcoords2: List[int]
    texcoords3: List[int]
    texcoords4: List[int]
    clut_id: int
    semitransp: int
    unknown: int
    
    def __init__(self, data: bytes):
        self.data = data
        stream = BytesIO(self.data)
        self.vertex_indices = [BinaryReader.read_uint8(stream) for _ in range(4)]
        self.texcoords1 = [BinaryReader.read_uint8(stream) for _ in range(2)]
        self.texcoords2 = [BinaryReader.read_uint8(stream) for _ in range(2)]
        self.texcoords3 = [BinaryReader.read_uint8(stream) for _ in range(2)]
        self.texcoords4 = [BinaryReader.read_uint8(stream) for _ in range(2)]
        self.clut_id = BinaryReader.read_uint16(stream)
        self.semitransp = BinaryReader.read_uint8(stream)
        self.unknown = BinaryReader.read_uint8(stream)
    
    def __repr__(self):
        return (f"Quad(vertices={self.vertex_indices}, "
                f"semitransp={bool(self.semitransp & 0x01)}, "
                f"clut_id={self.clut_id})")


@dataclass(init=False)
class Vertex:
    data: bytes
    x: int
    y: int
    z: int
    unknown: int
    
    def __init__(self, data: bytes):
        self.data = data
        stream = BytesIO(self.data)
        self.x = struct.unpack("<h", stream.read(2))[0]
        self.y = struct.unpack("<h", stream.read(2))[0]
        self.z = struct.unpack("<h", stream.read(2))[0]
        self.unknown = BinaryReader.read_uint16(stream)
    
    def __repr__(self):
        return f"Vertex(x={self.x}, y={self.y}, z={self.z})"


@dataclass(init=False)
class Model:
    triangle_count: int
    quad_count: int
    texture_page: int
    vertex_count: int
    triangles: List[Triangle]
    quads: List[Quad]
    vertices: List[Vertex]
    
    def __init__(self, stream: BytesIO):
        print(stream.tell(), stream.getbuffer().nbytes)
        self.triangle_count = BinaryReader.read_uint16(stream)
        self.quad_count = BinaryReader.read_uint16(stream)
        self.texture_page = BinaryReader.read_uint16(stream)
        self.vertex_count = BinaryReader.read_uint16(stream)

        self.triangles = []
        for _ in range(self.triangle_count):
            triangle_data = BinaryReader.read_bytes(stream, 12)
            self.triangles.append(Triangle(triangle_data))
        
        self.quads = []
        for _ in range(self.quad_count):
            quad_data = BinaryReader.read_bytes(stream, 16)
            self.quads.append(Quad(quad_data))
        
        self.vertices = []
        for _ in range(self.vertex_count):
            vertex_data = BinaryReader.read_bytes(stream, 8)
            self.vertices.append(Vertex(vertex_data))
    
    def __repr__(self):
        return (f"Model(triangles={self.triangle_count}, "
                f"quads={self.quad_count}, "
                f"vertices={self.vertex_count}, "
                f"texture_page={self.texture_page})")