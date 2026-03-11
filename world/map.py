from world.tile import Tile, TileType
from world.plant import Plant, PlantType


class GameMap:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.tiles = [[Tile() for _ in range(width)] for _ in range(height)]
        self._generate_terrain()

    def _generate_terrain(self):
        import random
        for y in range(self.height):
            for x in range(self.width):
                rand = random.random()
                if rand < 0.1:
                    self.tiles[y][x] = Tile(TileType.TREE)
                elif rand < 0.15:
                    self.tiles[y][x] = Tile(TileType.ROCK)
                elif rand < 0.2:
                    self.tiles[y][x] = Tile(TileType.WATER)
                else:
                    self.tiles[y][x] = Tile(TileType.SOIL)

    def get_tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None

    def set_tile(self, x, y, tile):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = tile

    def is_valid_position(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def grow_plants(self):
        for y in range(self.height):
            for x in range(self.width):
                tile = self.tiles[y][x]
                if tile.plant and not tile.plant.is_ready_to_harvest():
                    tile.plant.grow()

    def to_dict(self):
        return {
            "width": self.width,
            "height": self.height,
            "tiles": [[tile.to_dict() for tile in row] for row in self.tiles]
        }

    @classmethod
    def from_dict(cls, data):
        width = data.get("width", 10)
        height = data.get("height", 10)
        game_map = cls(width, height)
        if "tiles" in data:
            for y in range(height):
                for x in range(width):
                    if y < len(data["tiles"]) and x < len(data["tiles"][y]):
                        game_map.tiles[y][x] = Tile.from_dict(data["tiles"][y][x])
        return game_map
