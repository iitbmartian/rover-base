#!/usr/bin/env python

from matplotlib import pyplot as plt
from IPython.display import clear_output
import numpy as np
from time import sleep
import rospy
from std_msgs.msg import Float64MultiArray

def gps_callback(inp):
    plt.xlim(0,500)
    plt.ylim(0,500)
    x = [0,0]
    y = [0,0]
    point = plt.plot(x,y,'ro')[0]
    plt.ion()
    plt.show()
    rover_x = inp.data[0]
    rover_y = inp.data[1]
    print(rover_x,rover_y)
    x = [rover_x,gps_x]
    y = [rover_y,gps_y]
    point.set_data(x,y)
    print(point)
    plt.pause(1)

if __name__=='__main__':
    rospy.init_node('GPS_Node')
    rospy.loginfo('Starting GPS Tracking Node')
    gps_x = float(input('What is the x coordinate? '))
    gps_y = float(input('What is the y coordinate? '))
    while not rospy.is_shutdown():
        rospy.Subscriber('/LatLon',Float64MultiArray,gps_callback)
        rospy.spin()


# x=[1,10]
# y=[1,10]
# plt.xlim(0,10)
# plt.ylim(0,10)
# point = plt.plot(x,y,'ro')[0]
# plt.ion()
# plt.show()
# for i in range(10):
#     x[1] -= 1
#     y[1] -= 1
#     point.set_data(x,y)
#     plt.pause(1)
