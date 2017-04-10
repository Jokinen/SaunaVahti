from camera_manager import Camera_manager
from Server_manager import Server_manager

class Saunavahti:
    def __init__(self):
        self.setup()
        self.start()

    def setup(self):
        self.running = False
        self.camera = Camera_manager()
        self.server = Server_manager()

    def start(self):
        self.running = True
        self.server.start()
        self.loop()

    def loop(self):
        self.camera.record()
