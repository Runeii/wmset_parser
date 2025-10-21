from dataclasses import dataclass
from .generic_script_section import GenericScriptSection

@dataclass(init=False)
class Section36(GenericScriptSection):
  name: str = "Extends generic scripts"