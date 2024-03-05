#!/usr/bin/env python

import rospy
from std_msgs.msg import String

arm_pub = rospy.Publisher('/rover/bio_arm_directives',String,queue_size=1)

def callback(key_inp):


if __name__=='__main__':
    rospy.init_node('Basestation_Bio_Arm_Node')
    rospy.loginfo('Starting Basestation Bio Arm Node')
    