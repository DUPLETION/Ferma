import json
import os
from game.game_manager import GameManager


class SaveManager:
    SAVE_FILE = "savegame.json"

    def save(self, game_manager):
        data = game_manager.to_dict()
        try:
            with open(self.SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    def load(self):
        if not os.path.exists(self.SAVE_FILE):
            return None
        try:
            with open(self.SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return GameManager.from_dict(data)
        except Exception as e:
            print(f"Error loading game: {e}")
            return None

    def delete_save(self):
        if os.path.exists(self.SAVE_FILE):
            os.remove(self.SAVE_FILE)
            return True
        return False
