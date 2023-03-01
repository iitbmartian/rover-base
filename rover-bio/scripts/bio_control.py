#!/usr/bin/env python
# license removed for brevity
import rospy
import getch
from std_msgs.msg import String

def function():
    pub = rospy.Publisher('bio_control', String, queue_size=10)
    rospy.init_node('bio_control', anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        control = getch.getch()
        pub.publish(str(control))
        rate.sleep()

if __name__ == '__main__':
    function()