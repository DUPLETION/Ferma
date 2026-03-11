import sys
import io


class SandboxedEnvironment:
    def __init__(self, game_api):
        self.game_api = game_api
        self.locals = {}
        self._setup_environment()

    def _setup_environment(self):
        safe_builtins = {
            "True": True,
            "False": False,
            "None": None,
            "len": len,
            "range": range,
            "str": str,
            "int": int,
            "bool": bool,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "min": min,
            "max": max,
            "abs": abs,
            "sum": sum,
            "enumerate": enumerate,
            "zip": zip,
            "reversed": reversed,
            "sorted": sorted,
            "any": any,
            "all": all,
            "isinstance": isinstance,
            "print": self._safe_print
        }

        self.locals = {
            "move_up": self.game_api.move_up,
            "move_down": self.game_api.move_down,
            "move_left": self.game_api.move_left,
            "move_right": self.game_api.move_right,
            "plant": self.game_api.plant,
            "harvest": self.game_api.harvest,
            "water": self.game_api.water,
            "is_empty": self.game_api.is_empty,
            "is_plant": self.game_api.is_plant,
            "can_harvest": self.game_api.can_harvest,
            "scan": self.game_api.scan,
            "get_position": self.game_api.get_position,
            "get_inventory": self.game_api.get_inventory,
            "print": self._safe_print
        }

        self.globals = {"__builtins__": safe_builtins}

    def _safe_print(self, *args):
        self.game_api.print(*args)

    def execute(self, code):
        self.game_api.clear_print_buffer()
        output = io.StringIO()
        error_output = io.StringIO()

        old_stdout = sys.stdout
        old_stderr = sys.stderr

        try:
            sys.stdout = output
            sys.stderr = error_output

            compiled = compile(code, "<string>", "exec")
            exec(compiled, self.globals, self.locals)

            sys.stdout = old_stdout
            sys.stderr = old_stderr

            print_output = output.getvalue()
            error_msg = error_output.getvalue()

            api_output = self.game_api.get_print_buffer()
            all_output = print_output
            if api_output:
                all_output += "\n".join(api_output)

            return {
                "success": True,
                "output": all_output,
                "error": error_msg
            }

        except Exception as e:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

            return {
                "success": False,
                "output": output.getvalue(),
                "error": str(e)
            }
