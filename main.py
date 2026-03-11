from ui.main_screen import FarmApp
import sys
import os

if __name__ == "__main__":
    try:
        app = FarmApp()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
