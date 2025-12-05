#!/usr/bin/env python3

import rospy
import time
from ros_game_msgs.msg import user_msg
from std_msgs.msg import Int64


class ResultNode:
    def __init__(self):
        # Create a subscriber to receive user information
        self.sub = rospy.Subscriber('/user_information', user_msg, self.user_info_callback)
        self.sub = rospy.Subscriber('/result_information', Int64, self.result_info_callback)
        rospy.loginfo("[RESULT NODE] initialized, waiting for user info...")

    def user_info_callback(self, msg):
        # Log the received user information
        rospy.loginfo("[RESULT NODE] Received user information: Name: %s, Username: %s, Age: %d", msg.name, msg.username, msg.age)

        # Store in variable
        self.user_username = msg.username

    def result_info_callback(self, msg):
        # Show username and result
        rospy.loginfo("[RESULT NODE] User: %s, Result: %d", self.user_username, msg.data)
        
if __name__ == '__main__':
    try:
        # Initialize the ROS node
        rospy.init_node('result_node')

        # Create an instance of ResultNode
        result_node = ResultNode()

        rospy.loginfo("ResultNode is running. Waiting for user information...")

        # Keep the node running
        rospy.spin()

    except rospy.ROSInterruptException:
        pass

