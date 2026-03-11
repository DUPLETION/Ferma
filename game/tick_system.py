import threading


class TickSystem:
    TICK_DURATION = 0.2

    def __init__(self):
        self.running = False
        self.thread = None
        self.callback = None

    def start(self, callback):
        self.callback = callback
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)

    def _run(self):
        while self.running:
            if self.callback:
                self.callback()
            import time
            time.sleep(self.TICK_DURATION)
