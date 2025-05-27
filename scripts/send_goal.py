#!/usr/bin/env python3

import rospy
import actionlib
from assignment_2_2024.msg import PlanningAction, PlanningGoal
from rt1_assignment2_p1.srv import SendGoal, SendGoalResponse  # Adjust the import if in a different package
import time

def handle_send_goal(req):
    client = actionlib.SimpleActionClient('/reaching_goal', PlanningAction)
    client.wait_for_server()

    goal = PlanningGoal()
    goal.target_pose.pose.position.x = req.x
    goal.target_pose.pose.position.y = req.y

    rospy.loginfo(f"Sending goal: x={req.x}, y={req.y}")
    client.send_goal(goal)

    client.wait_for_result()
    result = client.get_result()

    return SendGoalResponse(success=True, message="Goal reached successfully.")

def main():
    rospy.init_node('send_goal_service_node')
    service = rospy.Service('/send_goal', SendGoal, handle_send_goal)
    rospy.loginfo("Service '/send_goal' is ready.")
    rospy.spin()

if __name__ == '__main__':
    main()
