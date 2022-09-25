import datetime
from enum import Enum


class DataType(Enum):
    VOLTAGE = 1
    TEMPERATURE = 2
    HUMIDITY = 3


class SensorData:

    def __init__(self, sensor_id: int, data_type: DataType, data_value: float, read_on: datetime.datetime):
        self.sensor_id = sensor_id
        self.data_type = data_type
        self.data_value = data_value
        self.read_on = read_on

