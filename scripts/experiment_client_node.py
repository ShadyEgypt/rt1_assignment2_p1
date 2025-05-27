#!/usr/bin/env python3

import rospy
import time
import csv
from std_srvs.srv import Empty
from rt1_assignment2_p1.srv import SendGoal

# === Hardcoded Goal List ===
goals = [
    (1.0, 2.0), (2.0, 1.0), (3.0, 3.0), (0.0, 0.0), (4.0, 2.5),
    (2.5, 4.0), (3.0, 1.5), (1.5, 3.5), (4.5, 1.0), (0.5, 0.5),
    (3.5, 3.5), (2.0, 2.0), (1.0, 4.0), (4.0, 4.0), (0.0, 3.0),
    (3.0, 0.0), (1.5, 1.5), (2.5, 2.5), (3.5, 0.5), (0.5, 3.5),
    (4.0, 0.0), (0.0, 4.0), (1.0, 1.0), (2.0, 3.0), (3.0, 2.0),
    (2.0, 0.0), (0.0, 2.0), (4.5, 4.5), (4.5, 0.5), (0.5, 4.5)
]

csv_path = "goal_times.csv"

def main():
    rospy.init_node('experiment_client_node')
    rospy.wait_for_service('/send_goal')
    rospy.wait_for_service('/reset_positions')

    send_goal_srv = rospy.ServiceProxy('/send_goal', SendGoal)
    reset_srv = rospy.ServiceProxy('/reset_positions', Empty)

    with open(csv_path, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['experiment', 'x', 'y', 'duration'])

        for i, (x, y) in enumerate(goals, start=1):
            rospy.loginfo(f"Sending goal {i}: ({x}, {y})")

            start = time.time()

            try:
                res = send_goal_srv(x, y)
                if res.success:
                    duration = round(time.time() - start, 2)
                    writer.writerow([i, x, y, duration])
                    rospy.loginfo(f"Goal {i} reached in {duration} seconds")
                else:
                    writer.writerow([i, x, y, "FAILED"])
                    rospy.logwarn(f"Goal {i} failed: {res.message}")
            except rospy.ServiceException as e:
                writer.writerow([i, x, y, "ERROR"])
                rospy.logerr(f"Service call failed: {e}")
                continue

            try:
                reset_srv()
                rospy.loginfo("Robot reset to initial position.")
            except rospy.ServiceException as e:
                rospy.logerr(f"Reset failed: {e}")

            time.sleep(1)

    rospy.loginfo("All experiments completed.")

if __name__ == '__main__':
    main()
