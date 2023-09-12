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

class Banner:
    @staticmethod
    def show_banner():
        banner = '''
Wellcome to the
         ____            _           _     _  ___ _ _              _ _       _     
        |  _ \ _ __ ___ (_) ___  ___| |_  | |/ (_) | |_____      _(_) |_ ___| |__  
        | |_) | '__/ _ \| |/ _ \/ __| __| | ' /| | | / __\ \ /\ / / | __/ __| '_ \ 
        |  __/| | | (_) | |  __/ (__| |_  | . \| | | \__ \\ V  V /| | || (__| | | |
        |_|   |_|  \___// |\___|\___|\__| |_|\_\_|_|_|___/ \_/\_/ |_|\__\___|_| |_|
                      |__/                                                         

        © Geethaka Perera (LAZURUS)       
        '''
        print(banner)
