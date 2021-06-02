#!/usr/bin/env python

import time
import rospy
import serial
import sys
import struct
import codecs

from sensor_msgs.msg import Imu

rospy.init_node("serial_imu_node")

imuMsg = Imu()

# read basic information
port = rospy.get_param('~port', '/dev/ttyUSB0')
baudrate = int(rospy.get_param('~baudrate', '115200'))
topic = rospy.get_param('~topic', 'imu')
frame_id = rospy.get_param('~frame_id', 'imu_link')

pub = rospy.Publisher(topic, Imu, queue_size=1)

while not rospy.is_shutdown():
    try:
        rospy.loginfo("Opening %s baudrate %d...", port, baudrate)
        try:
            ser = serial.Serial(port=port, baudrate=baudrate, timeout=1)
        except (serial.serialutil.SerialException, OSError) as e:
            rospy.logerr("IMU not found at port " + port + ". Did you specify the correct port in the launch file?")
            time.sleep(2)
            continue

        seq = 0
        accel_factor = 9.806

        ser.flushInput()
        rospy.loginfo("Flushing first 200 IMU entries...")
        for x in range(0, 200):
            ser.readline()
        rospy.loginfo("Publishing IMU data...")

        errcount = 0
        while not rospy.is_shutdown():
            line = ser.readline()
            if not line.startswith(b'/') or not line.endswith(b'\r\n') or len(line) != 83: 
                rospy.logwarn("Bad IMU data or bad sync")
                errcount = errcount + 1
                if errcount > 10:
                    break
                continue

            errcount = 0
            line = line[1: -2]
            errcount = 0
            gx, gy, gz, ax, ay, az, qw, qx, qy, qz = struct.unpack('>ffffffffff', codecs.decode(codecs.decode(line, 'latin1'), 'hex'))

            imuMsg.linear_acceleration.x = ax * accel_factor
            imuMsg.linear_acceleration.y = ay * accel_factor
            imuMsg.linear_acceleration.z = az * accel_factor

            imuMsg.angular_velocity.x = gx
            imuMsg.angular_velocity.y = gy
            imuMsg.angular_velocity.z = gz

            imuMsg.orientation.x = qx
            imuMsg.orientation.y = qy
            imuMsg.orientation.z = qz
            imuMsg.orientation.w = qw

            imuMsg.header.stamp = rospy.Time.now()
            imuMsg.header.frame_id = frame_id
            imuMsg.header.seq = seq
            seq = seq + 1
            pub.publish(imuMsg)

    except (serial.serialutil.SerialException, OSError) as e:
        rospy.logerr("serial error %s", e)
        ser = None
        time.sleep(2)
