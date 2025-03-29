"""
.. module:: action_client_node
    :platform: Unix
    :synopsis: A ROS action client node for sending navigation goals and monitoring robot status.
.. moduleauthor:: Shady

This node interfaces with the `/reaching_goal` action server to send goals,
cancel them, retrieve feedback, and track the robot's movement using `/odom` messages.
It also interacts with a custom service `/get_last_target` to store and retrieve the last target location.

Subscribes to:
    - `/odom` (Odometry messages)

Publishes to:
    - `/robot_status` (Custom RobotStatus messages)

Action Server:
    - `/reaching_goal` (PlanningAction)

Service Client:
    - `/get_last_target` (GetLastTarget)
"""

import rospy
import actionlib
from assignment_2_2024.msg import PlanningAction, PlanningGoal
from nav_msgs.msg import Odometry
from rt1_assignment2_p1.msg import RobotStatus
from geometry_msgs.msg import Twist
from rt1_assignment2_p1.srv import GetLastTarget, GetLastTargetResponse

current_feedback = {'x': 0.0, 'y': 0.0, 'status': ""}
""" Dictionary to store the latest feedback from the action server.
"""

def odom_callback(msg: Odometry) -> None:
    """
    Callback function for the `/odom` topic. Extracts robot position and velocity
    and publishes it to the `/robot_status` topic.

    Args:
    msg: Odometry message containing the robot's position and velocity.
    """
    global status_pub
    position = msg.pose.pose.position
    velocity = msg.twist.twist

    status_msg = RobotStatus()
    status_msg.x = position.x
    status_msg.y = position.y
    status_msg.vel_x = velocity.linear.x
    status_msg.vel_z = velocity.angular.z
    
    status_pub.publish(status_msg)

def send_goal(x: float, y: float) -> None:
    """
    Sends a goal to the `/reaching_goal` action server.

    Args:
    x: Target x-coordinate
    y: Target y-coordinate
    """
    global client
    goal = PlanningGoal()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    client.send_goal(goal, done_cb=goal_done_callback, feedback_cb=goal_feedback_callback)
    set_last_target(x, y)
    rospy.loginfo(f"Sent goal: x={x}, y={y}")

def goal_done_callback(status: int, result) -> None:
    """
    Callback function triggered when the action goal completes.

    Args:
    status: Status of the goal execution
    result: Result returned by the action server
    """
    if status == actionlib.GoalStatus.SUCCEEDED:
        rospy.loginfo("Goal achieved successfully!")
    else:
        rospy.loginfo("Goal did not complete successfully.")

def goal_feedback_callback(feedback) -> None:
    """
    Callback function for action feedback, updates the current robot position.

    Args:
    feedback: Feedback message from the action server
    """
    current_feedback['x'] = feedback.actual_pose.position.x
    current_feedback['y'] = feedback.actual_pose.position.y
    current_feedback['status'] = feedback.stat

def cancel_goal() -> None:
    """
    Cancels the currently active goal.
    """
    global client
    client.cancel_goal()
    rospy.loginfo("Goal canceled!")

def get_last_target() -> None:
    """
    Calls the `/get_last_target` service to retrieve the last stored target coordinates.
    """
    rospy.wait_for_service('/get_last_target')
    try:
        get_last_target_service = rospy.ServiceProxy('/get_last_target', GetLastTarget)
        response = get_last_target_service(False, 0, 0)
        rospy.loginfo(f"Last target was: x={response.res_x}, y={response.res_y}")
    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")

def set_last_target(x: float, y: float) -> None:
    """
    Calls the `/get_last_target` service to store the last target coordinates.

    Args:
    x: x-coordinate of the last target
    y: y-coordinate of the last target
    """
    rospy.wait_for_service('/get_last_target')
    try:
        set_last_target_service = rospy.ServiceProxy('/get_last_target', GetLastTarget)
        response = set_last_target_service(True, x, y)
        if response.success:
            rospy.loginfo("Last target successfully updated.")
    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")

if __name__ == '__main__':
    rospy.init_node('action_client_node')
    
    client = actionlib.SimpleActionClient('/reaching_goal', PlanningAction)
    """ Definition of the client
    """
    client.wait_for_server()
    
    rospy.Subscriber('/odom', Odometry, odom_callback)
    """ Definition of a subscriber to /odom
    """
    status_pub = rospy.Publisher('/robot_status', RobotStatus, queue_size=10)
    """ Definition of a publisher to /robot_status
    """

    try:
        while not rospy.is_shutdown():
            command = input(
                "Enter a command:\n"
                "  'set' - Set a new goal\n"
                "  'cancel' - Cancel the current goal\n"
                "  'status' - Check the status of the current action\n"
                "  'feedback' - Check current feedback\n"
                "  'last' - Retrieve the last target coordinates\n"
                "  'exit' - Quit the program\n"
                "Your choice: "
            ).strip().lower()
            
            if command == 'set':
                if client.get_state() == actionlib.GoalStatus.ACTIVE:
                    rospy.loginfo("A goal is currently active, cancel it first!")
                else:
                    x = float(input("Enter target x: "))
                    y = float(input("Enter target y: "))
                    send_goal(x, y)
            elif command == 'cancel':
                cancel_goal()
            elif command == 'status':
                if client.get_state() == actionlib.GoalStatus.ACTIVE:
                    rospy.loginfo(f"Current Status: {current_feedback['status']}.")
                else:
                    rospy.loginfo("The action is not active")
            elif command == 'feedback':
                if client.get_state() == actionlib.GoalStatus.ACTIVE:
                    rospy.loginfo(f"Current position: x={current_feedback['x']}, y={current_feedback['y']}")
                else:
                    rospy.loginfo("The action is not active")
            elif command == 'last':
                get_last_target()
            elif command == 'exit':
                break
    except rospy.ROSInterruptException:
        pass
