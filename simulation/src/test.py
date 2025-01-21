#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class JointStatePublisher(Node):
    def __init__(self):
        super().__init__('joint_state_publisher')
        self.publisher = self.create_publisher(JointState, '/joint_states', 10)
        self.create_timer(0.5, self.publish_joint_states)  # Timer to publish every 0.5 seconds

    def publish_joint_states(self):
        joint_positions = [1.0, 0.5, -0.5, 0.8, 0.018, 0.018]  # Joint values in radians (replace x with a fixed value)
        
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['joint1', 'joint2', 'joint3', 'joint4', 'gripper_left_joint', 'gripper_right_joint']
        msg.position = joint_positions
        
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing joint positions: {joint_positions}')

def main(args=None):
    rclpy.init(args=args)
    node = JointStatePublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
