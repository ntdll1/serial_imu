#!/bin/bash
echo "remap the device serial port(ttyACM*) to serial_imu"
echo "serial_imu usb connection as /dev/serial_imu, check it using command: ls -l /dev|grep ttyACM"
echo "start copy serial_imu.rules to /etc/udev/rules.d/"
echo "`rospack find serial_imu`/scripts/serial_imu.rules"
sudo cp `rospack find serial_imu`/scripts/serial_imu.rules /etc/udev/rules.d
echo ""
echo "restarting udev..."
echo ""
sudo service udev reload
sudo service udev restart
echo "done"
