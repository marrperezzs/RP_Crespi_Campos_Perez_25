#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int64
from ros_game_msgs.msg import user_msg
from ros_game.srv import GetUserScore, GetUserScoreRequest


class ResultNode:
    def __init__(self):
        rospy.init_node("result_node_s", anonymous=False)

        self.user_info = None       # guardará el user_msg
        self.final_score = None     # guardará el Int64 del resultado

        # Suscriptores
        rospy.Subscriber("user_information", user_msg, self.user_callback)
        rospy.Subscriber("result_information", Int64, self.score_callback)

        # Cliente del servicio user_score
        rospy.loginfo("RESULT_NODE: esperando al servicio 'user_score'...")
        rospy.wait_for_service("user_score")
        self.user_score_client = rospy.ServiceProxy("user_score", GetUserScore)
        rospy.loginfo("RESULT_NODE: conectado al servicio 'user_score'.")

    def user_callback(self, msg: user_msg):
        self.user_info = msg
        rospy.loginfo("RESULT_NODE: recibido user_information: %s (%s)",
                      msg.name, msg.username)
        self.maybe_print_result()

    def score_callback(self, msg: Int64):
        self.final_score = msg.data
        rospy.loginfo("RESULT_NODE: recibido result_information: %d", self.final_score)
        self.maybe_print_result()

    def maybe_print_result(self):
        """Cuando tengamos usuario y score, llamamos al servicio y mostramos porcentaje."""
        if self.user_info is None or self.final_score is None:
            return

        # Preparar request al servicio
        req = GetUserScoreRequest()
        req.username = self.user_info.username

        try:
            resp = self.user_score_client(req)
        except rospy.ServiceException as e:
            rospy.logerr("RESULT_NODE: llamada a user_score falló: %s", e)
            return

        percentage = resp.score

        rospy.loginfo(
            "RESULT_NODE: Player %s scored %d points (%.2f%%)",
            self.user_info.username, self.final_score, percentage
        )

        # Mensaje bonito por terminal
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