#!/usr/bin/env python3

import rospy
from gazebo_msgs.srv import SetModelState, SetModelStateRequest
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty, EmptyResponse

def handle_reset(req):
    rospy.wait_for_service('/gazebo/set_model_state')
    try:
        proxy = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)

        msg = SetModelStateRequest()
        msg.model_state.model_name = "robot1"  # Replace with your model name
        msg.model_state.pose.position.x = 1.0
        msg.model_state.pose.position.y = 1.0
        msg.model_state.pose.position.z = 0.0
        msg.model_state.pose.orientation.w = 1.0
        msg.model_state.twist = Twist()
        msg.model_state.reference_frame = "world"

        result = proxy(msg)
        if result.success:
            rospy.loginfo("Robot position reset.")
        else:
            rospy.logwarn("Reset failed.")
    except rospy.ServiceException as e:
        rospy.logerr(f"Reset service call failed: {e}")

    return EmptyResponse()

def main():
    rospy.init_node('reset_position_service_node')
    rospy.Service('/reset_positions', Empty, handle_reset)
    rospy.loginfo("Service '/reset_positions' is ready.")
    rospy.spin()

if __name__ == '__main__':
    main()
