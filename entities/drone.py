class Drone:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.inventory = {
            "wheat": 0,
            "carrot": 0,
            "potato": 0,
            "wood": 0,
            "stone": 0
        }

    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy
        if game_map.is_valid_position(new_x, new_y):
            tile = game_map.get_tile(new_x, new_y)
            if tile.type.value not in ["tree", "rock", "water"]:
                self.x = new_x
                self.y = new_y
                return True
        return False

    def add_item(self, item_type, amount):
        if item_type in self.inventory:
            self.inventory[item_type] += amount

    def remove_item(self, item_type, amount):
        if item_type in self.inventory and self.inventory[item_type] >= amount:
            self.inventory[item_type] -= amount
            return True
        return False

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "inventory": self.inventory.copy()
        }

    @classmethod
    def from_dict(cls, data):
        drone = cls(data.get("x", 0), data.get("y", 0))
        if "inventory" in data:
            drone.inventory = data["inventory"].copy()
        return drone
