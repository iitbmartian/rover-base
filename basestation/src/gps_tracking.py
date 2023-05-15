#!/usr/bin/env python

from matplotlib import pyplot as plt
from IPython.display import clear_output
import numpy as np
from time import sleep
import rospy
from std_msgs.msg import Float64MultiArray

global location

def gps_callback(inp):
    plt.xlim(0,200)
    plt.ylim(0,200)
    x = [0,0]
    y = [0,0]
    point = plt.plot(x,y,'ro')[0]
    plt.ion()
    rover_x = [inp.data[0]]
    rover_y = [inp.data[1]]
    x = gps_x + rover_x
    y = gps_y + rover_y
    point.set_data(x,y)
    for j in range(location):
        plt.annotate('Loc'+str(j+1),(x[j],y[j]))
    print(point)
    plt.pause(1)

if __name__=='__main__':
    rospy.init_node('GPS_Node')
    rospy.loginfo('Starting GPS Tracking Node')
    location=0
    gps_x = []
    gps_y = []
    while True:
        exists = input('Is there a new Location? y/n: ')
        if exists == 'y':
            gps_x.append(float(input('What is the x coordinate? ')))
            gps_y.append(float(input('What is the y coordinate ')))
            location+=1
        else:
            break
    while not rospy.is_shutdown():
        plt.show()
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
