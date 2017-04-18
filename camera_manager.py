# -*- coding: iso-8859-1 -*-
import io
import socket
import struct
import time
import picamera
from temperature_manager import TEMP_manager

class Camera_manager:
    def __init__(self):
        self.temp = TEMP_manager()
        self.camera = picamera.PiCamera()

    def take_image(self):
        self.camera.resolution = (1024, 768)
        self.camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        self.camera.annotate_background = picamera.Color('black')
        byte_string = str(self.temp.get_temp_as_celsius()) + ' C (valmis' + str(self.temp.estimate_time()) + ' min kuluttua)'
        self.camera.annotate_text = byte_string.decode('utf-8')
        self.camera.capture('source.png')
