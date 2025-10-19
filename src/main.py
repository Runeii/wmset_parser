from file_header import FileHeader
from sections.section_13 import Section13
from sections.section_15 import Section15
from sections.section_31 import Section31
from sections.section_34 import Section34
from sections.section_41 import Section41
import os

## IMPORTANT NOTE: in documentation sections are 1 indexed, in code they are 0 indexed. So section 1 in docs is section 0 in code.
def process_file(filepath: str) -> None:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filepath} does not exist")

    with open(filepath, "rb") as f:
        file_data = f.read()

    file_header = FileHeader(file_data)
    
    ## Print offsets with index as key
    for i, offset in enumerate(file_header.offsets):
        print(f"Offset {i}: {offset}")

    ## Remember, zero indexed! Section 13 in Wiki is section 12 here.
    dialog_text = Section13(file_header.sections[13])
    models = Section15(file_header.sections[15])
    location_names = Section31(file_header.sections[31])
    draw_points = Section34(file_header.sections[34])
    object_textures = Section41(file_header.sections[41])
    
    for i, model in enumerate(models.models):
      texture = object_textures.textures[i]
      Section15.export_model_to_obj(model, f"../output/models/model_{i}.obj", texture)
      texture.save_png(f"../output/textures/texture_{i}.png")
      print(f"Exported model_{i}.obj with texture_{i}.png")



if __name__ == "__main__":
  test_file_path = "wmsetus.obj"
  os.system('cls' if os.name == 'nt' else 'clear')
  process_file(test_file_path)