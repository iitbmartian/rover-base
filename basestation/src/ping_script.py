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
    iter_time = rospy.Rate(1)
    while True:
        os.system("clear")
        if not (ping("192.168.69.15") and ping("192.168.69.2")):
            if not ping("192.168.69.15"):
                if not ping("192.168.69.2"):
                    if not ping("192.168.69.101"):
                        print()
                        print("ONBOARD ROUTER GAYA")
                        if not ping("192.168.69.254"):
                            print()
                            print("COMMS UD GAYA, INTERVENTION LE BC")
                            if not ping("192.168.69.1"):
                                print()
                                print("BAHAAR JAAKE RUCKUS THEEK KAR")
                                if not ping("192.168.69.100"):
                                    print()
                                    print("FORGET URC")
        else:
            print()
            print("CHAL RAHA, URC PODIUM")
        iter_time.sleep()
