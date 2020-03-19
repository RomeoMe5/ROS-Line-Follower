#!/usr/bin/env python
import roslib; roslib.load_manifest('line_follower')
import rospy
from std_msgs.msg import Int32

import cv2
import numpy as np

def talker():
    pub = rospy.Publisher('Camera', Int32)
    rospy.init_node('Camera_Node')
    cap = cv2.VideoCapture(-1)
    cap.set(3, 160)
    cap.set(4, 120)

    while not rospy.is_shutdown():
        flag, frame = cap.read()
        img = frame[60:120, 0:160]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
        blur = cv2.GaussianBlur(gray,(5,5),0)
        ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
        image, contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
        res = 0
        if len(contours) > 0:

            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            m00 = M['m00']
            m10 = M['m10']
            if m00 != 0:
                cx = int(m10/m00)
            else:
                cx = 80
            res = 80 - cx
            msg = Int32(res)
        rospy.loginfo(msg)
        pub.publish(msg)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
