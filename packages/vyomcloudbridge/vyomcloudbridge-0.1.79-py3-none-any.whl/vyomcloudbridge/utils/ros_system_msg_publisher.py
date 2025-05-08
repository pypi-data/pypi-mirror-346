import importlib
import json
import rclpy
import time

from rclpy.node import Node
from vyomcloudbridge.constants import topics_list


class RosSystemMsgPublisher(Node):
    def __init__(self):
        rclpy.init(args=None)
        super().__init__("ros_system_msg_publisher")
        self.msg_publishers = {}  # { topic_name : (publisher, msg_instance) }
        self.msg_type_to_topic = self._build_msg_type_to_topic_map()
        self.get_logger().info("ROS System Message Publisher Node started.")

    def _build_msg_type_to_topic_map(self):
        """Builds a mapping from message class name to topic name from topics_list."""
        msg_type_map = {}
        for attr_name in dir(topics_list):
            if attr_name.isupper():
                attr = getattr(topics_list, attr_name)
                if isinstance(attr, tuple) and len(attr) == 2:
                    msg_class, topic_name = attr
                    msg_type_map[msg_class.__name__] = topic_name
        return msg_type_map

    def get_message_class(self, msg_name):
        """Try to load message class from available packages."""
        for package in topics_list.MSG_PKGS:
            try:
                module = importlib.import_module(f"{package}.msg")
                msg_class = getattr(module, msg_name)
                self.get_logger().info(
                    f"Loaded message '{msg_name}' from package '{package}'"
                )
                return msg_class
            except (ModuleNotFoundError, AttributeError):
                continue
        raise AttributeError(
            f"Message '{msg_name}' not found in any of: {topics_list.MSG_PKGS}"
        )

    def setup_publisher(self, name=None, typ=None, msg_data=None):
        """Setup publisher and message instance."""
        if not typ or msg_data is None:
            raise ValueError("Message type and data must be provided.")

        msg_class = self.get_message_class(typ)
        topic_name = name or self.msg_type_to_topic.get(typ, typ.lower())

        publisher = self.create_publisher(msg_class, topic_name, 10)
        msg_instance = msg_class()

        if isinstance(msg_data, dict):
            for field, value in msg_data.items():
                if hasattr(msg_instance, field):
                    setattr(msg_instance, field, value)
                else:
                    self.get_logger().error(
                        f"Field '{field}' not found in message '{msg_class.__name__}'"
                    )
        elif hasattr(msg_instance, "data"):
            msg_instance.data = msg_data
        else:
            raise ValueError(f"Invalid message format for type '{typ}'")

        self.msg_publishers[topic_name] = (publisher, msg_instance)
        self.get_logger().info(
            f"Publisher created for topic '{topic_name}' with message type '{typ}'"
        )

    def publish_all(self):
        """Publish all initialized messages."""
        for topic, (publisher, msg_instance) in self.msg_publishers.items():
            try:
                self.get_logger().info(f"Publishing to '{topic}': {msg_instance}")
                publisher.publish(msg_instance)
                time.sleep(1)
            except Exception as e:
                self.get_logger().error(f"Error publishing on '{topic}': {str(e)}")

    def cleanup(self):
        rclpy.shutdown()


def main(args=None):
    ros_msg_publisher = RosSystemMsgPublisher()

    # Input JSON message definitions
    input_json = """
    [
        {
            "typ": "MissionStatus",
            "msg": {
                "mission_id": 42,
                "mission_status": 1,
                "user_id": 101,
                "bt_id": "navigate_tree",
                "mission_feedback": "Mission is currently in progress."
            }
        },
        {
            "typ": "Hello",
            "msg": {"gcsid": "hello"}
        },
        {
            "typ": "Dvid",
            "msg": {"device_id": 5005}
        },
        {
            "typ": "Auth",
            "msg": {"auth_key": "sample_auth_key"}
        },
        {
            "typ": "Accessinfo",
            "msg": {
                "end_time": 1714321230,
                "current_date": 1714321220,
                "user_id": 1001
            }
        },
        {
            "typ": "Access",
            "msg": {"encrypted": "sample_encrypted_text"}
        },
        {
            "typ": "Ack",
            "msg": {"msgid": "msg001", "chunk_id": 10}
        }
    ]
    """
    input_data = json.loads(input_json)

    # Setup all publishers
    for item in input_data:
        ros_msg_publisher.setup_publisher(
            typ=item["typ"],
            msg_data=item["msg"]
        )

    ros_msg_publisher.publish_all()
    ros_msg_publisher.destroy_node()
    ros_msg_publisher.cleanup()


if __name__ == "__main__":
    main()
