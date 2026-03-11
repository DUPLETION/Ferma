from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse

from ui.console import Console
from ui.code_editor import CodeEditor
from game.game_manager import GameManager
from game.tick_system import TickSystem
from scripting.api import GameAPI
from scripting.sandbox import SandboxedEnvironment
from save.save_manager import SaveManager


class TileWidget(Widget):
    def __init__(self, tile_type, plant=None, **kwargs):
        super().__init__(**kwargs)
        self.tile_type = tile_type
        self.plant = plant
        self._update_color()

    def _update_color(self):
        self.canvas.clear()
        colors = {
            "empty": (0.3, 0.3, 0.3, 1),
            "soil": (0.4, 0.25, 0.1, 1),
            "plant": (0.2, 0.5, 0.2, 1),
            "tree": (0.1, 0.4, 0.1, 1),
            "rock": (0.5, 0.5, 0.5, 1),
            "water": (0.2, 0.3, 0.8, 1),
        }
        color = colors.get(self.tile_type, (0.3, 0.3, 0.3, 1))
        with self.canvas:
            Color(*color)
            Rectangle(pos=self.pos, size=self.size)


class GameMapWidget(GridLayout):
    def __init__(self, game_manager, **kwargs):
        super().__init__(**kwargs)
        self.game_manager = game_manager
        self.cols = game_manager.game_map.width
        self.rows = game_manager.game_map.height
        self.tile_widgets = []
        self.drone_widget = None
        self._build_map()

    def _build_map(self):
        self.clear_widgets()
        self.tile_widgets = []
        game_map = self.game_manager.game_map
        for y in range(game_map.height):
            row = []
            for x in range(game_map.width):
                tile = game_map.get_tile(x, y)
                tile_type = tile.type.value
                tile_widget = TileWidget(tile_type, tile.plant)
                tile_widget.size_hint = (1, 1)
                self.add_widget(tile_widget)
                row.append(tile_widget)
            self.tile_widgets.append(row)
        self._update_drone()

    def _update_drone(self):
        if self.drone_widget:
            self.remove_widget(self.drone_widget)
        x = self.game_manager.drone.x
        y = self.game_manager.drone.y
        tile = self.tile_widgets[y][x]
        self.drone_widget = Widget(size_hint=(None, None), size=(40, 40))
        with self.drone_widget.canvas:
            Color(1, 0, 0, 1)
            Ellipse(pos=(0, 0), size=(40, 40))
        self.drone_widget.pos = (tile.x + tile.width/2 - 20, tile.y + tile.height/2 - 20)
        self.add_widget(self.drone_widget)

    def update(self):
        game_map = self.game_manager.game_map
        for y in range(game_map.height):
            for x in range(game_map.width):
                tile = game_map.get_tile(x, y)
                self.tile_widgets[y][x].tile_type = tile.type.value
                self.tile_widgets[y][x].plant = tile.plant
                self.tile_widgets[y][x]._update_color()
        self._update_drone()


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.game_manager = GameManager()
        self.game_manager.set_update_callback(self.on_game_update)
        self.tick_system = TickSystem()
        self.sandbox = None
        self.code_thread = None
        self.running_code = False

        self._build_ui()
        self._setup_game()

    def _build_ui(self):
        self.top_panel = BoxLayout(size_hint_y=None, height=40)
        self.add_widget(self.top_panel)
        self._build_resources_panel()

        self.map_container = BoxLayout()
        self.add_widget(self.map_container)

        self.bottom_panel = BoxLayout(orientation="vertical", size_hint_y=0.5)
        self.add_widget(self.bottom_panel)
        self._build_editor_panel()

    def _build_resources_panel(self):
        self.resource_labels = {}
        resources = ["Пшеница", "Дерево", "Камень", "Вода"]
        keys = ["wheat", "wood", "stone", "water"]
        for res, key in zip(resources, keys):
            lbl = Label(text=f"{res}: {self.game_manager.resources.get(key, 0)}")
            self.resource_labels[key] = lbl
            self.top_panel.add_widget(lbl)

    def _build_editor_panel(self):
        self.code_editor = CodeEditor(size_hint_y=0.7)
        self.bottom_panel.add_widget(self.code_editor)

        button_panel = BoxLayout(size_hint_y=None, height=40)
        self.bottom_panel.add_widget(button_panel)

        btn_run = Button(text="Запустить код", on_press=self.run_code)
        btn_stop = Button(text="Остановить", on_press=self.stop_code)
        btn_clear = Button(text="Очистить", on_press=self.clear_code)
        btn_save = Button(text="Сохранить", on_press=self.save_game)
        btn_load = Button(text="Загрузить", on_press=self.load_game)

        button_panel.add_widget(btn_run)
        button_panel.add_widget(btn_stop)
        button_panel.add_widget(btn_clear)
        button_panel.add_widget(btn_save)
        button_panel.add_widget(btn_load)

        self.console = Console(size_hint_y=0.3)
        self.bottom_panel.add_widget(self.console)

    def _setup_game(self):
        self.game_map_widget = GameMapWidget(self.game_manager)
        self.map_container.add_widget(self.game_map_widget)

    def on_game_update(self):
        self.update_resources()
        self.game_map_widget.update()

    def update_resources(self):
        for key, label in self.resource_labels.items():
            res_names = {"wheat": "Пшеница", "wood": "Дерево", "stone": "Камень", "water": "Вода"}
            label.text = f"{res_names[key]}: {self.game_manager.resources.get(key, 0)}"

    def run_code(self, instance):
        if self.running_code:
            return
        code = self.code_editor.text
        if not code.strip():
            return

        self.running_code = True
        self.game_manager.player_code = code

        self.game_api = GameAPI(self.game_manager)
        self.sandbox = SandboxedEnvironment(self.game_api)

        self.tick_system.start(self._on_tick)

        import threading
        self.code_thread = threading.Thread(target=self._execute_code, args=(code,))
        self.code_thread.daemon = True
        self.code_thread.start()

        self.console.append_text("Код запущен...")

    def _on_tick(self):
        pass

    def _execute_code(self, code):
        import time
        if not self.sandbox:
            self.console.append_text("Ошибка: sandbox не инициализирована", (1, 0, 0, 1))
            return
        lines = code.split("\n")
        for line in lines:
            if not self.running_code:
                break
            if line.strip():
                try:
                    result = self.sandbox.execute(line)
                    if result and result["output"]:
                        self.console.append_text(result["output"])
                    if result and result["error"]:
                        self.console.append_text(f"Ошибка: {result['error']}", (1, 0, 0, 1))
                except Exception as e:
                    self.console.append_text(f"Ошибка: {str(e)}", (1, 0, 0, 1))
            time.sleep(TickSystem.TICK_DURATION)
        self.running_code = False
        self.console.append_text("Выполнение завершено.")

    def stop_code(self, instance):
        self.running_code = False
        self.tick_system.stop()
        self.console.append_text("Код остановлен.", (1, 0.5, 0, 1))

    def clear_code(self, instance):
        self.code_editor.text = ""

    def save_game(self, instance):
        self.game_manager.player_code = self.code_editor.text
        save_manager = SaveManager()
        save_manager.save(self.game_manager)
        self.console.append_text("Игра сохранена.", (0, 1, 1, 1))

    def load_game(self, instance):
        save_manager = SaveManager()
        game = save_manager.load()
        if game:
            self.game_manager = game
            self.game_manager.set_update_callback(self.on_game_update)
            self.code_editor.text = self.game_manager.player_code
            self.map_container.clear_widgets()
            self.game_map_widget = GameMapWidget(self.game_manager)
            self.map_container.add_widget(self.game_map_widget)
            self.update_resources()
            self.console.append_text("Игра загружена.", (0, 1, 1, 1))
        else:
            self.console.append_text("Не удалось загрузить игру.", (1, 0, 0, 1))


class FarmApp(App):
    def build(self):
        return MainScreen()


if __name__ == "__main__":
    FarmApp().run()
