from app.device.sensor import Sensor


class DeviceManager:

    def __init__(self, sensors: list[Sensor]):
        self.__sensors__ = sensors

    def get_n_sensor(self):
        return len(self.__sensors__)

    def read_device(self, n_device):
        try:
            return self.__sensors__[n_device].read_voltage()
        except Exception:
            return None

    def get_max_read(self, n_device):
        return self.__sensors__[n_device].get_max_read()

    def get_min_read(self, n_device):
        return self.__sensors__[n_device].get_min_read()

    def get_sensor_id(self, n_device):
        return self.__sensors__[n_device].get_sensor_id()


