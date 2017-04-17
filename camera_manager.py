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

    def take_image(self):
        camera = picamera.PiCamera()
        camera.resolution = (1024, 768)
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text = self.temp.get_temp_as_celsius() + '(arvioitu tavoitelämpötila saavutetaan' + self.temp.estimate_time() + 'kuluttua)'
        camera.capture('source.png')
