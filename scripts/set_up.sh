echo "install dependencies python and gpio"
sudo apt-get update --allow-releaseinfo-change -y
sudo apt-get update  -y
sudo apt-get upgrade -y
sudo apt-get install python3-pip
sudo pip3 install --upgrade setuptools
pip install RPI.GPIO
pip install adafruit-blinka
sudo pip3 install jproperties
sudo pip install --upgrade adafruit-python-shell

echo "Read serial number and store in home"
cat /sys/firmware/devicetree/base/serial-number > serial_number

echo "Create services to run code at boot time"
touch /lib/systemd/system/sensor_read.service

echo -e "[Unit]\n\nDescription=My Sample Service\nAfter=multi-user.target\n\n[Service]\n\nType=idle\nExecStart=/usr/bin/python /home/pi/main.py\n\n[Install]\n\nWantedBy=multi-user.target\n" > | sudo tee -a /lib/systemd/system/sensor_read.service


echo "start daemons for new service"
sudo systemctl daemon-reload
sudo systemctl enable sensor_read.service
sudo systemctl daemon-reload
sudo systemctl restart sensor_read

echo "please restart raspberry"