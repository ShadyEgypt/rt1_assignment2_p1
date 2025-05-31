#!/usr/bin/env python3

import rospy
import actionlib
import csv
import os
import time
from assignment_2_2024.msg import PlanningAction, PlanningGoal
from rt1_assignment2_p1.srv import SendGoal, SendGoalResponse

csv_file = "goal_times_client.csv"

def initialize_goal_counter():
    """Read the last ID from the CSV file to continue numbering correctly."""
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'x', 'y', 'duration'])
        return 1

    try:
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            rows = list(reader)
            if rows:
                last_id = int(rows[-1][0])
                return last_id + 1
    except Exception as e:
        rospy.logwarn(f"Could not read existing CSV properly: {e}")
    
    return 1

goal_counter = initialize_goal_counter()

def handle_send_goal(req):
    global goal_counter

    client = actionlib.SimpleActionClient('/reaching_goal', PlanningAction)
    client.wait_for_server()

    goal = PlanningGoal()
    goal.target_pose.pose.position.x = req.x
    goal.target_pose.pose.position.y = req.y

    rospy.loginfo(f"Sending goal {goal_counter}: x={req.x}, y={req.y}")
    start_time = time.time()
    client.send_goal(goal)

    success = client.wait_for_result(timeout=rospy.Duration(120))
    duration = round(time.time() - start_time, 2) if success else -1

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([goal_counter, req.x, req.y, duration])

    if success:
        rospy.loginfo(f"Goal {goal_counter} reached in {duration} seconds.")
        response = SendGoalResponse(success=True, message="Goal reached successfully.")
    else:
        rospy.logwarn(f"Goal {goal_counter} failed to reach within 2 minutes.")
        response = SendGoalResponse(success=False, message="Goal timeout after 2 minutes.")

    goal_counter += 1
    return response

def main():
    rospy.init_node('send_goal_service_node')
    rospy.Service('/send_goal', SendGoal, handle_send_goal)
    rospy.loginfo("Service '/send_goal' is ready.")
    rospy.spin()

if __name__ == '__main__':
    main()
