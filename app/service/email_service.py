from app.repositoriy.sensor_data import SensorData
from smtplib import SMTP_SSL, SMTPException
from email.message import EmailMessage
import logging

class EmailService:

    def __init__(self):
        self.__sender__ = 'alessio.conese.to@gmail.com'
        self.__receiver__ = 'svilla90@gmail.com'
        pass

    def send_email(self, sensor_data: list[SensorData], raspberry_identifier: str):
        data = '\n'.join(map(lambda d: str(d.read_on) + ':\t' + str(d.data_value), sensor_data))

        content = "Read values are:\n{data_values}".format(data_values=data)
        logging.info('send message with content: ' + content)

        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = f'Sensor Data for raspberry {raspberry_identifier} and sensor {sensor_data[0].sensor_id}'
        msg['From'] = self.__sender__
        msg['To'] = self.__receiver__

        try:
            self.__start_session_and_send__(msg)
            logging.info("Successfully sent email")
        except SMTPException as ex:
            logging.info("Error: unable to send email")
            raise ex

    def __start_session_and_send__(self, message):
        # Create SMTP server for sending the mail
        server = SMTP_SSL('smtp.gmail.com', 465)  # use gmail with port
        server.ehlo()
        server.login(self.__sender__, 'zeintitjbrpdgckc')  # login with mail_id and password
        text = message.as_string()
        server.sendmail(self.__sender__, self.__receiver__, text)
        server.quit()
