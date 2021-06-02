#!/bin/bash

echo "delete remap the device serial port(ttyACM*) of serial_imu"
echo "sudo rm /etc/udev/rules.d/serial_imu.rules"
sudo rm /etc/udev/rules.d/serial_imu.rules
echo ""
echo "restarting udev..."
echo ""
sudo service udev reload
sudo service udev restart
echo "done"
