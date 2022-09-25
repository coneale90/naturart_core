import logging

from jproperties import Properties

from app.main_service import MainService
from app.repositoriy.postgres_db import Postgres


def __read_db_properties__() -> Properties:
    configs = Properties()
    with open('db.properties', 'rb') as read_prop:
        configs.load(read_prop)
    return configs


if __name__ == "__main__":
    logging.basicConfig(
        filename='/home/pi/reader.log',
        format='%(asctime)s %(levelname)-8s %(message)s',
        filemode='a',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file1 = open('/home/pi/serial_number', 'r')
    lines = file1.readlines()
    raspberry_identifier = lines[0].rstrip('\x00').lstrip('\x00')
    logging.info("raspberry_identifier: " + raspberry_identifier)
    db_configs = __read_db_properties__()
    db = Postgres(
        db_url=db_configs.get('DB_URL')[0],
        db_user=db_configs.get('DB_USER')[0],
        db_password=db_configs.get('DB_PASSWORD')[0],
        db_name=db_configs.get('DB_NAME')[0],
        db_schema=db_configs.get('DB_SCHEMA')[0]
    )
    ms = MainService(raspberry_identifier, db)
    ms.start_reading_sensors()


