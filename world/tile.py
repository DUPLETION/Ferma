from enum import Enum


class TileType(Enum):
    EMPTY = "empty"
    SOIL = "soil"
    PLANT = "plant"
    TREE = "tree"
    ROCK = "rock"
    WATER = "water"


class Tile:
    def __init__(self, tile_type=TileType.EMPTY, plant=None):
        self.type = tile_type
        self.plant = plant

    def to_dict(self):
        data = {"type": self.type.value}
        if self.plant:
            data["plant"] = self.plant.to_dict()
        return data

    @classmethod
    def from_dict(cls, data):
        tile_type = TileType(data.get("type", "empty"))
        plant = None
        if "plant" in data and data["plant"]:
            from world.plant import Plant, PlantType
            plant = Plant.from_dict(data["plant"])
        return cls(tile_type, plant)
