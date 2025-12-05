#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import pygame

FPS = 60

class ControlNode:
    def __init__(self):
        self.pub = rospy.Publisher('/keyboard_control', String, queue_size=10)
        rospy.loginfo("ControlNode initialized (pygame), publishing to /keyboard_control")

        pygame.init()
        # Ventana pequeña para que pygame reciba foco y capture teclas
        self.screen = pygame.display.set_mode((320, 120))
        pygame.display.set_caption("ROS Control Node (Arrow Keys)")
        self.clock = pygame.time.Clock()

        # Para evitar spamear el mismo comando cada frame
        self.last_sent = None

    def publish_cmd(self, cmd: str):
        if cmd != self.last_sent:
            self.pub.publish(String(cmd))
            self.last_sent = cmd
            rospy.loginfo("Published movement command: %s", cmd)

    def main(self):
        running = True
        while running and not rospy.is_shutdown():
            self.clock.tick(FPS)

            # For our game only the up movements work but we defined all arrow keys to comply with the requirement
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.publish_cmd("UP")
                    elif event.key == pygame.K_DOWN:
                        self.publish_cmd("DOWN")
                    elif event.key == pygame.K_LEFT:
                        self.publish_cmd("LEFT")
                    elif event.key == pygame.K_RIGHT:
                        self.publish_cmd("RIGHT")
                    elif event.key == pygame.K_SPACE:
                        self.publish_cmd("JUMP")
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        running = False

            # Teclas mantenidas (movimiento continuo izq/der)
            keys = pygame.key.get_pressed()
            held = None
            if keys[pygame.K_LEFT]:
                held = "LEFT"
            elif keys[pygame.K_RIGHT]:
                held = "RIGHT"

            if held:
                self.publish_cmd(held)
            else:
                self.last_sent = None  # libera para permitir publicar otra vez al re-pulsar

            # Dibujito mínimo (opcional)
            self.screen.fill((20, 20, 20))
            pygame.display.flip()

        pygame.quit()
        rospy.loginfo("ControlNode exiting.")

if __name__ == '__main__':
    try:
        rospy.init_node('control_node')
        node = ControlNode()
        node.main()
    except rospy.ROSInterruptException:
        pass
