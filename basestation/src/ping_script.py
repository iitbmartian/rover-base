#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from math import *
import tf
import os
import signal
import sys

import rospy
from serial.serialutil import SerialException as SerialException


# SIGINT Handler to escape loops. Use Ctrl-C to exit
def sigint_handler(signal, frame):
    sys.exit(0)


def ping(hostname):
    response = os.system("ping -c 1 -t 1 " + hostname)
    if response != 0:
        print(hostname + "'s connection is weak")
        return False
    else:
        print(hostname + " is connected")
        return True


if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)
    rospy.init_node("Ping_Node")
    rospy.loginfo("Starting Ping Node")
    iter_time = rospy.Rate(0.2)
    while True:
        os.system("clear")

        if not (ping("192.168.69.15") and ping("192.168.69.2")):
            ping("192.168.69.15")
            ping("192.168.69.2")
            ping("192.168.69.101")
            ping("192.168.69.254")
            ping("192.168.69.1")
            ping("192.168.69.100")
        else:
            print("NUC and RPi Connected!!")
        print()
        ping("192.168.69.202")
        print()
        ping("192.168.69.203")
        print()
        ping("192.168.69.204")
        print()
        iter_time.sleep()
