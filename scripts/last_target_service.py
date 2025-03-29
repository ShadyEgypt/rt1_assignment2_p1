#!/usr/bin/env python3

"""
.. module:: last_target_service
    :platform: Unix
    :synopsis: A ROS service node for storing and retrieving the last target coordinates.
.. moduleauthor:: Shady

This node provides a ROS service `/get_last_target`, which allows other nodes to either
set a new last target or retrieve the previously stored target coordinates.

Service Server:
    - `/get_last_target` (:class:`rt1_assignment2_p1.srv.GetLastTarget`)
"""

import rospy
from rt1_assignment2_p1.srv import GetLastTarget, GetLastTargetResponse

last_target = {'x': 0.0, 'y': 0.0}
""" Dictionary to store the last target coordinates.
"""
def handle_last_target(req):
    """
    Callback function for the `/get_last_target` service.
    
    If `set_target` is True, updates the last target coordinates.
    Otherwise, returns the last stored coordinates.

    Args:
    :param req: Service request containing `set_target`, `x`, and `y`
    :type req: rt1_assignment2_p1.srv.GetLastTargetRequest
    
    :return: Response containing stored or updated coordinates
    :rtype: rt1_assignment2_p1.srv.GetLastTargetResponse
    """
    global last_target
    if req.set_target:
        last_target['x'] = req.x
        last_target['y'] = req.y
        rospy.loginfo(f"Set last target to x={req.x}, y={req.y}")
        return GetLastTargetResponse(res_x=req.x, res_y=req.y, success=True)
    else:
        rospy.loginfo("Returning last target coordinates.")
        return GetLastTargetResponse(res_x=last_target['x'], res_y=last_target['y'], success=True)

if __name__ == '__main__':
    rospy.init_node('last_target_service')

    service = rospy.Service('/get_last_target', GetLastTarget, handle_last_target)
    """ Service server for handling last target storage and retrieval
    """
    rospy.loginfo("Service /get_last_target is ready.")
    rospy.spin()
