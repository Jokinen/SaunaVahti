import RPi.GPIO as GPIO
import math
import time
import datetime as dt
import smbus

class TEMP_manager:
    def __init__(self):
        self.recorded_temps = []
        self.target_temp = 90
        self.setup()

    def setup(self):
        self.bus = smbus.SMBus(0)    # I2C bus, using B rev1 so parameter is 0

        # TCN75A address, 0x48(72) (found with i2cdetect -y 0)
        # Select configuration register, 0x01(01)
        #		0x60(96)	12-bit ADC resolution
        self.bus.write_byte_data(0x48, 0x01, 0x60)

        time.sleep(0.5)

    def read(self):
        # TCN75A address, 0x48(72)
        # Read data back from 0x00(00), 2 bytes
        # temp MSB, temp LSB
        data = self.bus.read_i2c_block_data(0x48, 0x00, 2)

        return data

    def convert_data(self):
        data = self.read()

        # Convert the data to 12-bits
        temp = ((data[0] * 256) + (data[1] & 0xF0)) / 16
        if temp > 2047 :
          temp -= 4096

        return temp

    def get_temp_as_celsius(self):
        temp = self.convert_data()
        converted_temp = temp * 0.0625
        t = dt.datetime.now()
        self.recorded_temps.append({
            'temp': converted_temp,
            'time': time.mktime(t.timetuple())
        })

        return converted_temp

    def estimate_time(self):
        skip = len(self.recorded_temps) <= 1

        if skip:
            return 'undef'

        average_increase = reduce(lambda x,y: x['temp'] + y['temp'], self.recorded_temps)
        average_time = reduce(lambda x,y: y['time'] + x['time'], self.recorded_temps) - self.recorded_temps[0]['time']

        last_temp = self.recorded_temps[len(self.recorded_temps) - 1]
        temps_to_go = self.target_temp - last_temp['temp']

        ticks = temps_to_go / average_increase
        time_to_go = ticks * average_time.total_seconds()

        return str(math.ceil(time_to_go / 60))
