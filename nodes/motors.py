#!/usr/bin/env python

import serial
import time
import rospy
import roslib; roslib.load_manifest('line_follower')
from line_follower.msg import Speed


ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()


def callback(data):
	global ser
	rospy.loginfo("A: %d B: %d" % (data.motorA, data.motorB))
	A =  data.motorA
	B = data.motorB
	if A  > 255:
		A = 255
	if B > 255:
		B = 255
	if A < -255:
		A = -255
	if B < -255:
		B = -255
	
	S = bytes("256 " + str(A) + " " + str(B) + " ")
	ser.write(S)


def listener():
	rospy.init_node('My_Motor_Node', anonymous=True)
	rospy.Subscriber("Motors", Speed, callback)
	rospy.spin()


if __name__ == '__main__':
	listener()
