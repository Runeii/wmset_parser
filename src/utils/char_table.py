####
###
##    This is a straight Claude conversion of the character table class from Deling. Nothing original.
###
####

from dataclasses import dataclass, field
from typing import Dict, List, ClassVar, Optional


@dataclass
class CharTable:
    """Character table for converting bytes to strings using FF8 text encoding."""
    
    # Character names
    NAMES: ClassVar[List[str]] = [
        "{Squall}", "{Zell}", "{Irvine}", "{Quistis}", "{Rinoa}", "{Selphie}",
        "{Seifer}", "{Edea}", "{Laguna}", "{Kiros}", "{Ward}", "{Angelo}", 
        "{Griever}", "{Boko}"
    ]
    
    # Color codes
    COLORS: ClassVar[List[str]] = [
        "{Darkgrey}", "{Grey}", "{Yellow}", "{Red}", "{Green}", "{Blue}", 
        "{Purple}", "{White}", "{DarkgreyBlink}", "{GreyBlink}", "{YellowBlink}",
        "{RedBlink}", "{GreenBlink}", "{BlueBlink}", "{PurpleBlink}", "{WhiteBlink}"
    ]
    
    # Location names
    LOCATIONS: ClassVar[List[str]] = [
        "{Galbadia}", "{Esthar}", "{Balamb}", "{Dollet}", 
        "{Timber}", "{Trabia}", "{Centra}", "{Horizon}"
    ]
    
    # Default character lookup table (table 0)
    DEFAULT_CHAR_TABLE: ClassVar[Dict[int, str]] = {
        0x00: "t",
        0x02: "\n",
        0x03: "_AngeloVar",
        0x04: "_UnknownVariable2",
        0x0E: "_UnknownVariable3",
        0x20: " ",
        0x21: "0",
        0x22: "1",
        0x23: "2",
        0x24: "3",
        0x25: "4",
        0x26: "5",
        0x27: "6",
        0x28: "7",
        0x29: "8",
        0x2A: "9",
        0x2B: "%",
        0x2C: "/",
        0x2D: ":",
        0x2E: "!",
        0x2F: "?",
        0x30: "…",
        0x31: "+",
        0x32: "-",
        0x33: "SPECIAL CHARACTER TODO",
        0x34: "*",
        0x35: "&",
        0x36: "SPECIAL CHARACTER TODO",
        0x37: "SPECIAL CHARACTER TODO",
        0x38: "(",
        0x39: ")",
        0x3A: "SPECIAL CHARACTER TODO",
        0x3B: ".",
        0x3C: ",",
        0x3D: "~",
        0x3E: "SPECIAL CHARACTER TODO",
        0x3F: "SPECIAL CHARACTER TODO",
        0x40: "'",
        0x41: "#",
        0x42: "$",
        0x43: "`",
        0x44: "_",
        0x45: "A",
        0x46: "B",
        0x47: "C",
        0x48: "D",
        0x49: "E",
        0x4A: "F",
        0x4B: "G",
        0x4C: "H",
        0x4D: "I",
        0x4E: "J",
        0x4F: "K",
        0x50: "L",
        0x51: "M",
        0x52: "N",
        0x53: "O",
        0x54: "P",
        0x55: "Q",
        0x56: "R",
        0x57: "S",
        0x58: "T",
        0x59: "U",
        0x5A: "V",
        0x5B: "W",
        0x5C: "X",
        0x5D: "Y",
        0x5E: "Z",
        0x5F: "a",
        0x60: "b",
        0x61: "c",
        0x62: "d",
        0x63: "e",
        0x64: "f",
        0x65: "g",
        0x66: "h",
        0x67: "i",
        0x68: "j",
        0x69: "k",
        0x6A: "l",
        0x6B: "m",
        0x6C: "n",
        0x6D: "o",
        0x6E: "p",
        0x6F: "q",
        0x70: "r",
        0x71: "s",
        0x72: "t",
        0x73: "u",
        0x74: "v",
        0x75: "w",
        0x76: "x",
        0x77: "y",
        0x78: "z",
        0x79: "Ł",
        0x7C: "Ä",
        0x88: "Ó",
        0x8A: "Ö",
        0x8E: "Ü",
        0x90: "ß",
        0x94: "ä",
        0xA0: "ó",
        0xA2: "ö",
        0xA6: "ü",
        0xA8: "Ⅷ",
        0xA9: "[",
        0xAA: "]",
        0xAB: "[SQUARE]",
        0xAC: "@",
        0xAD: "[SSQUARE]",
        0xAE: "{",
        0xAF: "}",
        0xC6: "Ⅵ",
        0xC7: "Ⅱ",
        0xC9: "™",
        0xCA: "<",
        0xCB: ">",
        0xE8: "in",
        0xE9: "e ",
        0xEA: "ne",
        0xEB: "to",
        0xEC: "re",
        0xED: "HP",
        0xEE: "l ",
        0xEF: "ll",
        0xF0: "GF",
        0xF1: "nt",
        0xF2: "il",
        0xF3: "o ",
        0xF4: "ef",
        0xF5: "on",
        0xF6: " w",
        0xF7: " r",
        0xF8: "wi",
        0xF9: "fi",
        0xFB: "s ",
        0xFC: "ar",
        0xFE: " S",
        0xFF: "ag"
    }
    
    # Instance variable for character tables (can have multiple tables for Japanese)
    tables: List[List[str]] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize with default character table if none provided."""
        if not self.tables:
            # Create default table from the lookup dictionary
            # Tables store characters from 0x20 onwards
            default_table = [''] * 224  # 256 - 0x20 = 236 slots
            for byte_val, char in self.DEFAULT_CHAR_TABLE.items():
                if byte_val >= 0x20:
                    default_table[byte_val - 0x20] = char
            self.tables = [default_table]
    
    def caract(self, ord_val: int, table: int = 0) -> str:
        """
        Get character from specified table.
        
        Args:
            ord_val: Byte value
            table: Table index (0 for default, 1-3 for Japanese tables)
            
        Returns:
            Character string or empty string if not found
        """
        if table < len(self.tables) and ord_val >= 0x20:
            return self.tables[table][ord_val - 0x20]
        return ''
    
    @staticmethod
    def getTextFromBytes(data: bytes, tables: Optional[List[List[str]]] = None) -> str:
        """
        Convert FF8 encoded bytes to string.
        
        Args:
            data: FF8 encoded bytes
            tables: Optional character tables (for Japanese support)
            
        Returns:
            Decoded string
        """
        decoder = CharTable(tables=tables if tables else [])
        return decoder.fromFF8(data)
    
    def fromFF8(self, ff8_bytes: bytes) -> str:
        """
        Decode FF8 byte string to text.

        
        Args:
            ff8_bytes: Bytes to decode
            
        Returns:
            Decoded string with control codes
        """
        result = []
        jp = len(self.tables) == 4  # Japanese version has 4 tables
        i = 0
        
        while i < len(ff8_bytes):
            byte = ff8_bytes[i]
            
            if byte == 0x00:  # End of string
                break
            elif byte == 0x01:  # New page
                result.append("\n{NewPage}\n")
            elif byte == 0x02:  # Newline
                result.append("\n")
            elif byte == 0x03:  # Character name
                i += 1
                if i < len(ff8_bytes):
                    index = ff8_bytes[i]
                    if 0x30 <= index <= 0x3A:
                        result.append(self.NAMES[index - 0x30])
                    elif index == 0x40:
                        result.append(self.NAMES[11])  # Angelo
                    elif index == 0x50:
                        result.append(self.NAMES[12])  # Griever
                    elif index == 0x60:
                        result.append(self.NAMES[13])  # Boko
                    else:
                        result.append(f"{{x03{index:02x}}}")
                else:
                    result.append("{x03}")
            elif byte == 0x04:  # Variables
                i += 1
                if i < len(ff8_bytes):
                    index = ff8_bytes[i]
                    if 0x20 <= index <= 0x27:
                        result.append(f"{{Var{index - 0x20}}}")
                    elif 0x30 <= index <= 0x37:
                        result.append(f"{{Var0{index - 0x30}}}")
                    elif 0x40 <= index <= 0x47:
                        result.append(f"{{Varb{index - 0x40}}}")
                    else:
                        result.append(f"{{x04{index:02x}}}")
                else:
                    result.append("{x04}")
            elif byte == 0x06:  # Colors
                i += 1
                if i < len(ff8_bytes):
                    index = ff8_bytes[i]
                    if 0x20 <= index <= 0x2F:
                        result.append(self.COLORS[index - 0x20])
                    else:
                        result.append(f"{{x06{index:02x}}}")
                else:
                    result.append("{x06}")
            elif byte == 0x09:  # Wait/pause
                i += 1
                if i < len(ff8_bytes):
                    index = ff8_bytes[i]
                    if index >= 0x20:
                        result.append(f"{{Wait{index - 0x20:03d}}}")
                    else:
                        result.append(f"{{x09{index:02x}}}")
                else:
                    result.append("{x09}")
            elif byte == 0x0E:  # Location
                i += 1
                if i < len(ff8_bytes):
                    index = ff8_bytes[i]
                    if 0x20 <= index <= 0x27:
                        result.append(self.LOCATIONS[index - 0x20])
                    else:
                        result.append(f"{{x0e{index:02x}}}")
                else:
                    result.append("{x0e}")
            elif jp and 0x19 <= byte <= 0x1B:  # Japanese tables
                i += 1
                if i < len(ff8_bytes):
                    old_index = byte
                    index = ff8_bytes[i]
                    if index >= 0x20:
                        character = self.caract(index, old_index - 0x18)
                    else:
                        character = ''
                    if not character:
                        character = f"{{x{old_index:02x}{index:02x}}}"
                    result.append(character)
                else:
                    result.append(f"{{x{byte:02x}}}")
            elif byte == 0x1C:  # Japanese additional
                i += 1
                if i < len(ff8_bytes):
                    index = ff8_bytes[i]
                    if index >= 0x20:
                        result.append(f"{{Jp{index - 0x20:03d}}}")
                    else:
                        result.append(f"{{x1c{index:02x}}}")
                else:
                    result.append("{x1c}")
            elif 0x05 <= byte <= 0x1F:  # Other two-byte control sequences
                i += 1
                if i < len(ff8_bytes):
                    result.append(f"{{x{byte:02x}{ff8_bytes[i]:02x}}}")
                else:
                    result.append(f"{{x{byte:02x}}}")
            else:  # Regular character lookup
                character = self.caract(byte)
                if character:
                    result.append(character)
                else:
                    result.append(f"{{x{byte:02x}}}")
            
            i += 1
        
        return ''.join(result)