#!/usr/bin/env python3
import rospy
import time
from std_msgs.msg import String


class ControlNode:
    def __init__(self):
        # Create a publisher to publish user information
        self.pub = rospy.Publisher('/keyboard_control', String, queue_size=10)
        rospy.loginfo("ControlNode initialized, ready to publish user info.")
        #wait for the publisher to be ready
        #time.sleep(5)

        #call the main function
        self.main()

    def main(self):
        #loops waiting for input of movements
        while not rospy.is_shutdown():
            command = input("Enter your movement command (w/a/s/d for up/left/down/right (not usefull) or space for jumping): ")
            if command == 'w':
                self.pub.publish('UP')
                rospy.loginfo("Published movement command: %s", command)
            elif command == 'a':
                self.pub.publish('LEFT')
                rospy.loginfo("Published movement command: %s", command)
            elif command == 's':
                self.pub.publish('DOWN')
                rospy.loginfo("Published movement command: %s", command)
            elif command ==    'd':
                self.pub.publish('RIGHT')
                rospy.loginfo("Published movement command: %s", command)
            elif command == ' ':
                self.pub.publish('JUMP')
                rospy.loginfo("Published movement command: %s", command)
            elif command == 'q':
                rospy.loginfo("Quitting control node.")
                break
            
            else:
                rospy.loginfo("Invalid command. Please enter w/a/s/d or q to quit.")
        

if __name__ == '__main__':
    try:
        # Initialize the ROS node
        rospy.init_node('control_node')
        # Create an instance of ControlNode
        control_node = ControlNode()

    except rospy.ROSInterruptException:
        pass