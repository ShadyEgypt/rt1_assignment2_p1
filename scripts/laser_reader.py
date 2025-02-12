#! /usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
from std_srvs.srv import *

import math

active_ = False
pub_ = None
pub_closest_ = None  # Publisher for the closest distance
regions_ = {
    'right': 0,
    'fright': 0,
    'front': 0,
    'fleft': 0,
    'left': 0,
}

def wall_follower_switch(req):
    global active_
    active_ = req.data
    res = SetBoolResponse()
    res.success = True
    res.message = 'Done!'
    return res

def clbk_laser(msg):
    global regions_
    regions_ = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[144:287]), 10),
        'front':  min(min(msg.ranges[288:431]), 10),
        'fleft':  min(min(msg.ranges[432:575]), 10),
        'left':   min(min(msg.ranges[576:713]), 10),
    }

    # Calculate and publish the closest distance
    closest_distance = min(regions_.values())
    pub_closest_.publish(Float32(closest_distance))

    take_action()

def main():
    global pub_, pub_closest_, active_

    rospy.init_node('reading_laser')

    pub_ = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    pub_closest_ = rospy.Publisher('/closest_obstacle', Float32, queue_size=10)  # Initialize the new publisher

    sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)
    srv = rospy.Service('wall_follower_switch', SetBool, wall_follower_switch)

    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        if not active_:
            rate.sleep()
            continue

        rate.sleep()

if __name__ == '__main__':
    main()
