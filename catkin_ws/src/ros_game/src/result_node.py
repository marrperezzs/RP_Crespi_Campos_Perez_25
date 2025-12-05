#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int64
from ros_game_msgs.msg import user_msg
from ros_game.srv import GetUserScore, GetUserScoreRequest


class ResultNode:
    def __init__(self):
        rospy.init_node("result_node_s", anonymous=False)

        self.user_info = None       # for the user_msg
        self.final_score = None     # for the Int64 result

        # Subscribers
        rospy.Subscriber("user_information", user_msg, self.user_callback)
        rospy.Subscriber("result_information", Int64, self.score_callback)

        # Service client for user_score
        rospy.loginfo("[RESULT_NODE] waiting for 'user_score' service...")
        rospy.wait_for_service("user_score")

        self.user_score_client = rospy.ServiceProxy("user_score", GetUserScore)
        rospy.loginfo("[RESULT_NODE] connected to 'user_score' service.")

    def user_callback(self, msg: user_msg):
        self.user_info = msg
        rospy.loginfo("[RESULT_NODE] received user_information: %s (%s)",
                      msg.name, msg.username)
        self.maybe_print_result()

    def score_callback(self, msg: Int64):
        self.final_score = msg.data
        rospy.loginfo("[RESULT_NODE] received result_information: %d", self.final_score)
        self.maybe_print_result()

    def maybe_print_result(self):
        """When we have both user and score, call the service and display percentage."""
        if self.user_info is None or self.final_score is None:
            return

        # Prepare request to the service
        req = GetUserScoreRequest()
        req.username = self.user_info.username

        try:
            resp = self.user_score_client(req)
        except rospy.ServiceException as e:
            rospy.logerr("[RESULT_NODE] call to user_score failed: %s", e)
            return

        percentage = resp.score

        rospy.loginfo(
            "[RESULT_NODE] Player %s scored %d points (%.2f%%)",
            self.user_info.username, self.final_score, percentage
        )

        # Nice message for the terminal
        print("\n====================================")
        print(" Player {} ({})".format(self.user_info.username, self.user_info.name))
        print(" Score: {} points ({:.2f} %)".format(self.final_score, percentage))
        print("====================================\n")


if __name__ == "__main__":
    try:
        node = ResultNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass