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
        self.save_temp(converted_temp)

        return converted_temp

    def save_temp(self, converted_temp):
        t = dt.datetime.now()
        self.recorded_temps.append({
            'temp': converted_temp,
            'time': time.mktime(t.timetuple())
        })

        if len(self.recorded_temps) > 3:
            # only keep track of last three measurements
            self.recorded_temps = self.recorded_temps[-3:]

    def estimate_time(self):
        skip = len(self.recorded_temps) <= 1

        if skip:
            return 'undef'

        datapoint_count = len(self.recorded_temps)

        first_measure = self.recorded_temps[len(self.recorded_temps) - 1]['time']
        last_measure = self.recorded_temps[0]['time']
        complete_time_increase = first_measure - last_measure
        average_time_increase = (complete_time_increase) / datapoint_count
        print('Average time between measurements: ' + str(average_time_increase) + 's')

        last_temp = 0
        temp_growth_s = []
        print('Saved temps:')
        for temp in self.recorded_temps:
            temp_dif = temp['temp'] - last_temp
            last_temp = temp['temp']
            growth_speed = (temp_dif / average_time_increase) if last_temp is not 0 else 0 
            temp_growth_s.append(growth_speed)
            print('Temp: ' + str(temp['temp']) + '. At time: ' + str(temp['time']) + '. Speed: ' + str(growth_speed))
        print('End of saved temps.')

        # C/s
        average_temp_growth_s = reduce(lambda x, y: x + y, temp_growth_s) / len(temp_growth_s)
        print('average temp growth speed: ' + str(average_temp_growth_s))

        last_temp = self.recorded_temps[len(self.recorded_temps) - 1]
        temps_to_go = self.target_temp - last_temp['temp']
        print('Temps until finished: ' + str(temps_to_go))

        seconds_to_go = temps_to_go / average_temp_growth_s
        min_to_go = seconds_to_go / 60
        print('Minutes until finished: ' + str(min_to_go))

        return str(math.ceil(min_to_go))
