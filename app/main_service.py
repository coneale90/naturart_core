from app.service.device_manager import DeviceManager
from app.service.email_service import EmailService
from app.repositoriy.postgres_db import Postgres
from app.repositoriy.sensor_data import SensorData, DataType
from app.device.sensor import Sensor
from datetime import datetime
import logging
import time


class MainService:

    def __init__(self, raspberry_identifier, db):
        self.__raspberry_identifier__ = raspberry_identifier
        self.__es__ = EmailService()
        self.__db__ = db

        self.__dm__ = DeviceManager(self.get_sensors(raspberry_identifier))
        if self.__dm__.get_n_sensor() == 0:
            raise Exception("No sensors found for current raspberry with identifier: " + raspberry_identifier)
        logging.info("Number of sensors found: " + str(self.__dm__.get_n_sensor()))
        self.__sensor_data__ = []
        self.start_reading_sensors()

    def start_reading_sensors(self):
        while True:
            try:
                for i in range(self.__dm__.get_n_sensor()):
                    voltage = self.__dm__.read_device(i)
                    if voltage is None:
                        logging.info('Impossible to read from sensor: ' + str(i))
                    else:
                        logging.info('read voltage: ' + str(voltage))
                        sensor_data = SensorData(
                            self.__dm__.get_sensor_id(i),
                            DataType.VOLTAGE,
                            voltage,
                            datetime.now()
                        )
                        self.__sensor_data__.append(sensor_data)
                        self.__db__.insert_sensor_data([sensor_data])
                        self.__db__.update_sensor_min_max(
                            self.__dm__.get_sensor_id(i),
                            self.__dm__.get_min_read(i),
                            self.__dm__.get_max_read(i)
                        )
                        logging.info("min max updated")
                        if len(self.__sensor_data__) > 24:
                            logging.info("sending email")
                            self.__es__.send_email(self.__sensor_data__, self.__raspberry_identifier__)
                            self.__sensor_data__.clear()
                            logging.info("email sent")
                logging.info("sleep time")
                time.sleep(3600)
            except Exception:
                logging.exception("Something went wrong")

    def get_sensors(self, raspberry_identifier):
        sensors = []
        result_sensor = self.__db__.find_sensor_on_raspberry(raspberry_identifier)
        for r in result_sensor:
            s = Sensor(
                sensor_id=r[0],
                min_v=r[1],
                max_v=r[2],
                pin_number=r[3]
            )
            logging.info("Found sensor " + str(s.__sensor_id__) + " connected to pin number: " + str(s.__pin_number__))
            sensors.append(s)

        return sensors
