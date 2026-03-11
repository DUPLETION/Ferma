from world.map import GameMap
from entities.drone import Drone
from world.tile import TileType
from world.plant import Plant, PlantType


class GameManager:
    def __init__(self):
        self.game_map = GameMap(10, 10)
        self.drone = Drone(5, 5)
        self.resources = {
            "wheat": 10,
            "wood": 5,
            "stone": 2,
            "water": 100
        }
        self.player_code = ""
        self.is_running = False
        self.on_update = None

    def set_update_callback(self, callback):
        self.on_update = callback

    def move_drone(self, dx, dy):
        moved = self.drone.move(dx, dy, self.game_map)
        if self.on_update:
            self.on_update()
        return moved

    def plant_seed(self, seed_type):
        tile = self.game_map.get_tile(self.drone.x, self.drone.y)
        if tile and tile.type == TileType.SOIL and not tile.plant:
            try:
                plant_type = PlantType(seed_type)
                tile.plant = Plant(plant_type)
                tile.type = TileType.PLANT
                if self.on_update:
                    self.on_update()
                return True
            except ValueError:
                pass
        return False

    def harvest(self):
        tile = self.game_map.get_tile(self.drone.x, self.drone.y)
        if tile and tile.plant and tile.plant.is_ready_to_harvest():
            plant_type = tile.plant.type.value
            self.drone.add_item(plant_type, 1)
            tile.plant = None
            tile.type = TileType.SOIL
            if self.on_update:
                self.on_update()
            return True
        return False

    def water(self):
        tile = self.game_map.get_tile(self.drone.x, self.drone.y)
        if self.resources.get("water", 0) > 0 and tile and tile.type == TileType.SOIL:
            self.resources["water"] -= 1
            if tile.plant:
                if tile.plant.growth_stage < Plant.GROWTH_STAGES - 1:
                    tile.plant.grow()
                    tile.plant.grow()
            if self.on_update:
                self.on_update()
            return True
        return False

    def is_empty(self):
        tile = self.game_map.get_tile(self.drone.x, self.drone.y)
        return tile and tile.type == TileType.EMPTY

    def is_plant(self):
        tile = self.game_map.get_tile(self.drone.x, self.drone.y)
        return tile and tile.type == TileType.PLANT

    def can_harvest(self):
        tile = self.game_map.get_tile(self.drone.x, self.drone.y)
        return tile and tile.plant and tile.plant.is_ready_to_harvest()

    def scan(self):
        directions = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0)
        }
        result = {}
        for direction, (dx, dy) in directions.items():
            x = self.drone.x + dx
            y = self.drone.y + dy
            tile = self.game_map.get_tile(x, y)
            if tile:
                result[direction] = tile.type.value
            else:
                result[direction] = "empty"
        return result

    def get_position(self):
        return (self.drone.x, self.drone.y)

    def get_inventory(self):
        return self.drone.inventory.copy()

    def tick(self):
        self.game_map.grow_plants()
        if self.on_update:
            self.on_update()

    def to_dict(self):
        return {
            "map": self.game_map.to_dict(),
            "drone": self.drone.to_dict(),
            "resources": self.resources.copy(),
            "player_code": self.player_code
        }

    @classmethod
    def from_dict(cls, data):
        game = cls()
        if "map" in data:
            game.game_map = GameMap.from_dict(data["map"])
        if "drone" in data:
            game.drone = Drone.from_dict(data["drone"])
        if "resources" in data:
            game.resources = data["resources"].copy()
        if "player_code" in data:
            game.player_code = data["player_code"]
        return game
