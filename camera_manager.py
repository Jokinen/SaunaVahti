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

    def connect(self):
        # Connect a client socket to my_server:8000 (change my_server to the
        # hostname of your server)
        client_socket = socket.socket()
        client_socket.connect(('my_server', 8002))

        return client_socket

    def record(self):
        # Make a file-like object out of the connection
        client_socket = self.connect()

        # Make a file-like object out of the connection
        connection = client_socket.makefile('wb')
        try:
            with picamera.PiCamera() as camera:
                camera.resolution = (640, 480)
                camera.framerate = 24
                # Start a preview and let the camera warm up for 2 seconds
                camera.start_preview()
                time.sleep(2)
                # Start recording, sending the output to the connection for 60
                # seconds, then stop
                camera.start_recording(connection, format='h264')
                camera.wait_recording(60)
                camera.stop_recording()
        finally:
            connection.close()
            client_socket.close()

        # stream = io.BytesIO()
        # with picamera.PiCamera() as camera:
        #     camera.resolution = (640, 480)
        #     camera.annotate_background = picamera.Color('black')
        #     camera.annotate_text = self.temp.get_temp_as_celsius() + '(arvioitu tavoitelämpötila saavutetaan' + self.temp.estimate_time() + 'kuluttua)'
        #     camera.start_recording(stream, format='h264', quality=23)
        #     camera.wait_recording(15)
        #     camera.stop_recording()
