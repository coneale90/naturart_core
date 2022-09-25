from app.repositoriy.sensor_data import SensorData
from psycopg2.extras import execute_values
import logging
import psycopg2


class Postgres:

    def __init__(self, db_url, db_user, db_password, db_name, db_schema, db_port=5432):
        self.db_name = db_name
        self.db_url = db_url
        self.db_user = db_user
        self.db_password = db_password
        self.db_port = db_port
        self.db_schema = db_schema
        self.__init_database__()

    def __init_database__(self):
        self.__connection__ = psycopg2.connect(
            database=self.db_name,
            host=self.db_url,
            user=self.db_user,
            password=self.db_password,
            port=self.db_port,
            options="-c search_path=" + self.db_schema
        )

    def insert_sensor_data(self, sensor_data: list[SensorData]):
        self.__reinit_db_connection__()
        logging.info('Start to store data in database')
        sql = 'INSERT INTO device_sensor_data (sensor_id, data_type, data_value, read_on) VALUES %s'
        to_insert = list(map(lambda d: (d.sensor_id, d.data_type.value, d.data_value, d.read_on), sensor_data))
        with self.__connection__.cursor() as cur:
            execute_values(cur, sql, to_insert)
            self.__connection__.commit()
        logging.info('Successfully stored data in database')
        self.__close_db_connection__()

    def find_sensor_on_raspberry(self, raspberry_identifier: str):
        self.__reinit_db_connection__()
        sql = """
            SELECT s.id, s.sensor_min_value, s.sensor_max_value, rsc.pin_number
            FROM sensor_info s, raspberry_sensor_connection rsc
            WHERE s.id = rsc.sensor_id and rsc.raspberry_id in (
                SELECT ri.id
                FROM raspberry_info ri
                WHERE ri.identifier = %s
            ) 
            AND rsc.removed_on is null
            ;
        """
        with self.__connection__.cursor() as cur:
            cur.execute(sql, (raspberry_identifier,))
            result = cur.fetchall()
            self.__close_db_connection__()
            return result

    def update_sensor_min_max(self, sensor_id, min_value, max_value):
        self.__reinit_db_connection__()
        logging.info('Start to update min max in database')
        sql = """
                   UPDATE sensor_info s
                   SET sensor_min_value = %s, sensor_max_value = %s
                   WHERE s.id = %s
                   ;
            """
        with self.__connection__.cursor() as cur:
            cur.execute(sql, (min_value, max_value, sensor_id,))
            self.__connection__.commit()
        logging.info('Successfully updated min max in database')
        self.__close_db_connection__()

    def __reinit_db_connection__(self):
        if self.__connection__ is None or self.__connection__.closed > 0:
            self.__init_database__()

    def __close_db_connection__(self):
        try:
            if self.__connection__ is not None:
                self.__connection__.close()
        except Exception:
            self.__connection__ = None

