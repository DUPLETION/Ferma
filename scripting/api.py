class GameAPI:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self._print_buffer = []

    def move_up(self):
        return self.game_manager.move_drone(0, -1)

    def move_down(self):
        return self.game_manager.move_drone(0, 1)

    def move_left(self):
        return self.game_manager.move_drone(-1, 0)

    def move_right(self):
        return self.game_manager.move_drone(1, 0)

    def plant(self, seed):
        return self.game_manager.plant_seed(seed)

    def harvest(self):
        return self.game_manager.harvest()

    def water(self):
        return self.game_manager.water()

    def is_empty(self):
        return self.game_manager.is_empty()

    def is_plant(self):
        return self.game_manager.is_plant()

    def can_harvest(self):
        return self.game_manager.can_harvest()

    def scan(self):
        return self.game_manager.scan()

    def get_position(self):
        return self.game_manager.get_position()

    def get_inventory(self):
        return self.game_manager.get_inventory()

    def print(self, *args):
        message = " ".join(str(arg) for arg in args)
        self._print_buffer.append(message)

    def get_print_buffer(self):
        return self._print_buffer

    def clear_print_buffer(self):
        self._print_buffer = []
