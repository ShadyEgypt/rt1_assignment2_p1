#!/usr/bin/env python3

import rospy
import csv
from std_srvs.srv import Empty
from rt1_assignment2_p1.srv import SendGoal
import os

input_goal_file = "assignment2.csv"

def read_goals_from_csv(file_path):
    goals = []
    if not os.path.isfile(file_path):
        rospy.logerr(f"CSV file '{file_path}' not found.")
        return []

    with open(file_path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2:
                try:
                    x = float(row[0].strip())
                    y = float(row[1].strip())
                    goals.append((x, y))
                except ValueError:
                    rospy.logwarn(f"Skipping invalid row: {row}")
    return goals

def main():
    rospy.init_node('experiment_client_node')
    rospy.wait_for_service('/send_goal')
    rospy.wait_for_service('/reset_positions')

    send_goal_srv = rospy.ServiceProxy('/send_goal', SendGoal)
    reset_srv = rospy.ServiceProxy('/reset_positions', Empty)

    goals = read_goals_from_csv(input_goal_file)
    if not goals:
        rospy.logerr("No valid goals loaded. Exiting.")
        return

    for i, (x, y) in enumerate(goals, start=1):
        rospy.loginfo(f"Sending goal {i}: ({x}, {y})")

        try:
            res = send_goal_srv(x, y)
            if res.success:
                rospy.loginfo(f"Goal {i} reached successfully.")
            else:
                rospy.logwarn(f"Goal {i} failed: {res.message}")
        except rospy.ServiceException as e:
            rospy.logerr(f"Service call failed for goal {i}: {e}")
            continue

        try:
            reset_srv()
            rospy.loginfo("Robot reset to initial position.")
        except rospy.ServiceException as e:
            rospy.logerr(f"Reset failed: {e}")

        rospy.sleep(1)

    rospy.loginfo("All goals sent.")

if __name__ == '__main__':
    main()
