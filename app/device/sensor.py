import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class Sensor:

    def __init__(self, pin_number: int, sensor_id: int, max_v=1.42, min_v=1.2):
        self.__pin_number__ = pin_number
        if pin_number == 0:
            self.__pin__ = ADS.P0
        elif pin_number == 1:
            self.__pin__ = ADS.P1
        elif pin_number == 2:
            self.__pin__ = ADS.P2
        elif pin_number == 3:
            self.__pin__ = ADS.P3
        else:
            raise Exception("Sorry, pin allowed are from p0 to p3")
        self.__sensor_id__ = sensor_id
        self.__max_read__ = max_v
        self.__min_read__ = min_v
        self.__init_channel_()

    def __init_channel_(self):
        # Create the I2C bus
        self.__i2c__ = busio.I2C(board.SCL, board.SDA)

        self.__ads__ = ADS.ADS1015(self.__i2c__)
        self.__chan__ = AnalogIn(self.__ads__, self.__pin__)

    def read_voltage(self):
        vol = self.__chan__.voltage
        if vol > self.__max_read__:
            self.__max_read__ = vol
        elif vol < self.__min_read__:
            self.__min_read__ = vol
        return vol

    def get_sensor_id(self):
        return self.__sensor_id__

    def get_min_read(self):
        return self.__min_read__

    def get_max_read(self):
        return self.__max_read__


