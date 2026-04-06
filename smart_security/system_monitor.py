import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
import os

class SystemMonitor(Node):
    def __init__(self):
        super().__init__('system_monitor')

        # Dictionary to track statistics for all main topics
        self.stats = {
            '/camera_frames': 0,
            '/detected_objects': 0,
            '/object_depth': 0,
            '/scene_analysis': 0,
            '/security_event': 0,
            '/security_alert': 0
        }

        self.create_subscription(Image, '/camera_frames', 
            lambda msg: self.count_msg('/camera_frames'), 10)
        
        self.create_subscription(String, '/detected_objects', 
            lambda msg: self.count_msg('/detected_objects'), 10)
        
        self.create_subscription(String, '/object_depth', 
            lambda msg: self.count_msg('/object_depth'), 10)
        
        self.create_subscription(String, '/scene_analysis', 
            lambda msg: self.count_msg('/scene_analysis'), 10)
        
        self.create_subscription(String, '/security_event', 
            lambda msg: self.count_msg('/security_event'), 10)
        
        self.create_subscription(String, '/security_alert', 
            lambda msg: self.count_msg('/security_alert'), 10)

        self.timer = self.create_timer(1.0, self.display_status)

    def count_msg(self, topic_name):
        self.stats[topic_name] += 1

    def display_status(self):
        os.system('cls' if os.name == 'nt' else 'clear') # clear terminal

        print("=" * 30)
        print("=== SYSTEM HEALTH MONITOR ===")
        print("=" * 30)
        
        for topic, count in self.stats.items():
            status = "ACTIVE" if count > 0 else "WAITING..."
            print(f"{topic:20} | Msgs: {count:4} | Status: {status}")
        


def main(args=None):
    rclpy.init(args=args)
    node = SystemMonitor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()