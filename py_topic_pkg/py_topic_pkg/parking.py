# Copyright 2021 Seoul Business Agency Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python3

import sys
import rclpy
from rclpy.node import Node
# message type
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class ParkingNode(Node):
    def __init__(self):
        super().__init__('parking_node')

        queue_size = 10
        self.publisher = self.create_publisher(
            Twist, 'skidbot/cmd_vel', queue_size
        )
        self.subscriber = self.create_subscription(
            LaserScan, 'skidbot/scan', self.sub_callback, queue_size
        )
        self.publisher  # prevent unused variable warning
        self.subscriber # prevent unused variable warning

        self.get_logger().info('=== Parking Node Start ===\n')

    def sub_callback(self, msg):
        twist_msg = Twist()
        distance_forward = msg.ranges[360]

        if distance_forward > 0.3: #[m]
            self.get_logger().info(
                f'Distance from Front Object : {distance_forward}'
            )
            twist_msg.linear.x = 0.5
            self.publisher.publish(twist_msg)

        else:
            self.get_logger().info(
                '=== Parking Done ===\n'
            )
            twist_msg.linear.x = 0.0
            self.publisher.publish(twist_msg)

def main(args=None):
    rclpy.init(args=args)

    parking_node = ParkingNode()

    try:
        rclpy.spin(parking_node)
    except KeyboardInterrupt:
        print("=== Server stopped cleanly ===")
    except BaseException:
        print("!! Exception in server:", file=sys.stderr)
        raise
    finally:
        # (optional, Done automatically when node is garbege collected)
        rclpy.shutdown()

if __name__ == "__main__":
    main()