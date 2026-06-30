from dataclasses import dataclass, field
from typing import Literal

@dataclass
class Tile:
    ColorPresent: Literal["black", "white", "none"]
    TileName : str
    TileColor: Literal["black", "white"]
    Symbol: str
    PiecePresent: Literal["Pa", "Ki", "Qu", "Bi", "Ro", "Kn", "No"] = "No"
    Pin : int = 0
    Pinning: int = -1
    CanPassant : int = -1