import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from security_interfaces.action import SecurityAction
import time

class AlarmController(Node):
    def __init__(self):
        super().__init__('alarm_controller')
        self._action_server = ActionServer(self, SecurityAction, 'security_action', self.execute_callback)
        self.get_logger().info("Alarm Controller Server is ready.")

    def execute_callback(self, goal_handle):
        command = goal_handle.request.command
        self.get_logger().info(f"Executing: {command}")

        steps = []

        if command == "trigger_alarm":
            steps = [
                "Initializing alarm...",
                "Activating siren...",
                "Alerting authorities...",
                "Alarm active"
            ]
        elif command == "alert_security":
            steps = [
                "Identifying threat...",
                "Alerting security..."
            ]
        elif command == "no_threats":
            steps = [
                "resetting system...",
                "system reset..."
            ]
        else:
            self.get_logger().warn(f"Unknown command received: {command}")
            goal_handle.abort()
            return SecurityAction.Result(success=False, message="Unknown command")    

        for step in steps:
            feedback_msg = SecurityAction.Feedback()
            feedback_msg.status = step

            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f"Feedback sent: {step}")
            time.sleep(0.5)

        goal_handle.succeed()
        result = SecurityAction.Result()
        result.success = True
        result.message = f"{command} completed"
        return result

def main(args=None):
    rclpy.init(args=args)
    node = AlarmController()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()