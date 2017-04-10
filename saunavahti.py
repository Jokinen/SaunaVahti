from camera_manager import Camera_manager

class Saunavahti:
    def __init__(self):
        self.setup()
        self.start()

    def setup(self):
        self.running = False
        self.camera = Camera_manager()

    def start(self):
        self.running = True
        self.loop()

    def loop(self):
        while self.running:
            pass
