import io
import time
import picamera
import TEMP_manager

class Camera_manager:
    def __init__(self):
        self.temp = TEMP_manager()

    def record(self):
        stream = io.BytesIO()
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.annotate_text = self.temp.get_temp_as_celsius() + '(arvioitu tavoitelämpötila saavutetaan' + self.temp.estimate_time() + 'kuluttua)'
            camera.start_recording(stream, format='h264', quality=23)
            camera.wait_recording(15)
            camera.stop_recording()
