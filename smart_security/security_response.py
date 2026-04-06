import rclpy
from rclpy.node import Node

from std_msgs.msg import String

from rclpy.action import ActionClient
from security_interfaces.action import SecurityAction


class SecurityResponse(Node):
    def __init__(self):
        super().__init__('security_response')

        # subscribers
        self.event_sub = self.create_subscription(String, '/security_event', self.event_callback, 10)

        # publishers
        self.alert_pub = self.create_publisher(String, '/security_alert', 10)

        # action client
        self._action_client = ActionClient(self, SecurityAction, '/security_action')

        # parameters
        self.declare_parameter('alert_level', 'HIGH') # declare alert level and set it to high
        self.alert_level = self.get_parameter('alert_level').value # stores the parameter value in an instance variable

        self.get_logger().info("Security response node is running.")

    def event_callback(self, msg):
        event = msg.data

        alert_msg = String()

        # check alert level
        if event == "clear":
            alert_msg.data = "threat cleared"
            self.send_action_goal("no_threats")
        else:
            if self.alert_level == "LOW":
                alert_msg.data = f"LOG: {event}"

            elif self.alert_level == "MEDIUM":
                alert_msg.data = f"WARNING: {event}"
                self.send_action_goal("alert_security")

            else:
                alert_msg.data = f"ALERT: {event}"
                self.send_action_goal("trigger_alarm")

        self.alert_pub.publish(alert_msg)

    # action client callback
    def send_action_goal(self, command):
            # check if server is running
            if not self._action_client.wait_for_server(timeout_sec=2.0):
                self.get_logger().warn("Action server not available!")
                return
            
            goal_msg = SecurityAction.Goal()
            goal_msg.command = command

            self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback.status
        self.get_logger().info(f"feedback: {feedback}")

def main(args=None):
    rclpy.init(args=args)
    node = SecurityResponse()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()