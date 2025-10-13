from .topicextractors import CameraImageTopicExtractor, LidarImageTopicExtractor



schema_to_extractor_mapping = {
	"sensor_msgs/msg/CompressedImage": CameraImageTopicExtractor,
	"sensor_msgs/msg/PointCloud2": LidarImageTopicExtractor,
	"nav_msgs/msg/Odometry": None
}


class TopicExtractorFactory:
	def __init__(self, export_root):
		self.export_root = export_root


	def create_from_config(self, topic_config):
		schema_name = topic_config["schema"]
		if schema_name in schema_to_extractor_mapping:
			extractor = schema_to_extractor_mapping[schema_name]
			return extractor(topic_config["alias"], self.export_root)
		else:
			return None