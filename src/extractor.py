from mcap.reader import make_reader
from mcap_ros2.decoder import DecoderFactory

from .core import load_config
from .schema import extractor_config_schema
from .extractor.topics import CameraImageTopic, LidarImageTopic


schema_to_extractor_mapping = {
	"sensor_msgs/msg/CompressedImage": CameraImageTopic,
	"sensor_msgs/msg/PointCloud2": LidarImageTopic,
	"nav_msgs/msg/Odometry": None
}


def main():
	config = load_config(schema=extractor_config_schema)
	# Get all required values from config
	required_topics = set([s["topic"] for s in config["sensors"]])
	# Todo: Check config content for additional details not verifiable with schema
	# Iterate through messages
	with open(config["rosbagPath"], "rb") as recording_file:
		reader = make_reader(recording_file, decoder_factories=[DecoderFactory()])
		for schema, channel, message, ros_msg in reader.iter_decoded_messages(topics=TOPIC_PATHS, start_time=START_TIME, end_time=END_TIME):
			pass
	

if __name__ == "__main__":
	main()