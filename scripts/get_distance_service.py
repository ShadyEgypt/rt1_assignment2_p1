#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
from rt1_assignment2_p1.srv import GetDistanceFromTarget, GetDistanceFromTargetResponse, GetLastTarget

position = {'x': 0.0, 'y': 0.0}
last_target = {'x': None, 'y': None}

def odom_callback(msg):
    global position
    position['x'] = msg.pose.pose.position.x
    position['y'] = msg.pose.pose.position.y

def calculate_distance(req):
    global last_target
    if last_target['x'] is None or last_target['y'] is None:
        return GetDistanceFromTargetResponse(0, 0, 0)

    target_x = last_target['x']
    target_y = last_target['y']
    distance = ((position['x'] - target_x)**2 + (position['y'] - target_y)**2)**0.5
    return GetDistanceFromTargetResponse(distance, target_x, target_y)

def update_last_target():
    rospy.wait_for_service('/get_last_target')
    try:
        get_last_target = rospy.ServiceProxy('/get_last_target', GetLastTarget)
        response = get_last_target(False, 0, 0)
        if response.success:
            global last_target
            last_target['x'] = response.res_x
            last_target['y'] = response.res_y
    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: %s" % e)

if __name__ == '__main__':
    rospy.init_node('distance_service')
    rospy.Subscriber('/odom', Odometry, odom_callback)
    update_last_target()
    service = rospy.Service('/get_distance_from_target', GetDistanceFromTarget, calculate_distance)
    rospy.loginfo("Distance service is ready.")
    rospy.spin()
