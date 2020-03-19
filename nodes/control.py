#!/usr/bin/env python
import roslib; roslib.load_manifest('line_follower')
import rospy
from line_follower.msg import Speed
from std_msgs.msg import Int32

try:
    	pub = rospy.Publisher('Motors', Speed)
    	rospy.init_node('Control_Node')
	speed = 115.0
	kp = 1.3
except rospy.ROSInterruptException: pass

def callback(data):
	global pub
	msg = Speed()
    	msg.motorA = int(speed + float(data.data) * kp)
    	msg.motorB = int(speed - float(data.data) * kp)
    	rospy.loginfo(msg)
    	pub.publish(msg)


def listener():
	rospy.loginfo("Listen\n")
#	rospy.init_node('My_Motor_Node', anonymous=True)
	rospy.Subscriber("Camera", Int32, callback)
	rospy.spin()

if __name__ == '__main__':
    try:
	    listener()
    except rospy.ROSInterruptException: pass
