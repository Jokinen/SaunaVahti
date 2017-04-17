from camera_manager import Camera_manager
from server_manager import Server_manager
import time

class Saunavahti:
    def __init__(self):
        self.setup()
        self.start()

    def setup(self):
        self.running = False
        self.camera = Camera_manager()
        # Server is started and it begins to serve this folder
        self.server = Server_manager()

    def start(self):
        self.running = True
        self.loop()

    def loop(self):
        while self.running:
            self.camera.take_image()
            time.sleep(1)
