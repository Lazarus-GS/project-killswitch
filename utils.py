import sys, time, threading, signal

class Loader:
    def __init__(self, count, delay):
        self.count = count
        self.delay = delay
        self.running = False
        self.loader_thread = None

    def _animate(self):
        while self.running:
            for _ in range(self.count):
                for _ in range(3):
                    sys.stdout.write('.')
                    sys.stdout.flush()
                    time.sleep(self.delay)
                sys.stdout.write('\b\b\b   \b\b\b')  # Clear three dots
                sys.stdout.flush()
                time.sleep(self.delay)

    def start(self, text):
        if not self.loader_thread:
            self.running = True
            sys.stdout.write(text)
            self.loader_thread = threading.Thread(target=self._animate)
            self.loader_thread.daemon = True
            self.loader_thread.start()

    def stop(self):
        if self.loader_thread:
            self.running = False
            self.loader_thread.join()
            self.loader_thread = None
            sys.stdout.write('\n')
            sys.stdout.flush()

class signalHandler:
    @staticmethod
    def handle_signal(sig, frame):
        print("\nExiting...")
        sys.exit(1)

    @classmethod
    def register_signal_handler(cls):
        signal.signal(signal.SIGINT, cls.handle_signal)