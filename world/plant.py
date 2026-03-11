from enum import Enum


class PlantType(Enum):
    WHEAT = "wheat"
    CARROT = "carrot"
    POTATO = "potato"


class Plant:
    GROWTH_STAGES = 3

    def __init__(self, plant_type, growth_stage=0):
        self.type = plant_type
        self.growth_stage = growth_stage

    def grow(self):
        if self.growth_stage < self.GROWTH_STAGES - 1:
            self.growth_stage += 1

    def is_ready_to_harvest(self):
        return self.growth_stage >= self.GROWTH_STAGES - 1

    def to_dict(self):
        return {
            "type": self.type.value,
            "growth_stage": self.growth_stage
        }

    @classmethod
    def from_dict(cls, data):
        plant_type = PlantType(data.get("type", "wheat"))
        return cls(plant_type, data.get("growth_stage", 0))
