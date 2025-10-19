bl_info = {
    "name": "WorldMap Extractor",
    "author": "A H",
    "version": (1, 0),
    "blender": (4, 3, 0),
    "location": "File > Import > WorldMap (.wmsetxx)",
    "description": "Import models from worldmap files",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}

import bpy
import os
import sys

# Add the addon directory to Python path
addon_dir = os.path.dirname(os.path.realpath(__file__))
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)

from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Context, Panel

# Import local modules
from src.main import process_file

class ImportWorldMap(bpy.types.Operator, ImportHelper):
    """Import from WorldMap (.wmsetxx)"""
    bl_idname = "ff8tools.worldmap"
    bl_label = "Import WorldMap"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".wmsetxx"
    filter_glob: StringProperty(default="*.wmsetxx", options={'HIDDEN'})

    def execute(self, context: 'Context') -> set[str]:
        process_file(self.filepath)
        return {'FINISHED'}

def menu_func_import(self: 'Panel', context: 'Context') -> None:
    if self.layout is not None:
        layout: UILayout = self.layout
        layout.operator(ImportWorldMap.bl_idname, text="WorldMap (.wmsetxx)")

def register() -> None:
    bpy.utils.register_class(ImportWorldMap)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister() -> None:
    bpy.utils.unregister_class(ImportWorldMap)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)  # type: ignore

if __name__ == "__main__":
    register() 