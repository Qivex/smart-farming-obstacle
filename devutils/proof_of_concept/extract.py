import sys, json, os
from time import time
from math import floor, sqrt
from struct import unpack

import numpy as np
import imageio
imageio.plugins.freeimage.download()

from mcap_ros2.decoder import DecoderFactory
from mcap.reader import make_reader



# Read args
arg_len = len(sys.argv)
if arg_len < 2:
	raise AttributeError("Path to .mcap file required!")

MCAP_PATH = sys.argv[1]

START_TIME = None
END_TIME = None
if arg_len > 3:
	START_TIME = int(sys.argv[2]) * 1e9
	END_TIME = int(sys.argv[3]) * 1e9

OUT_DIR = f"out-{floor(time())}"



# List of topics to export
class Topic:
	ODOM = "nav_msgs/msg/Odometry"
	IMG = "sensor_msgs/msg/CompressedImage"
	LIDAR = "sensor_msgs/msg/PointCloud2"

	def __init__(self, name, schema, path):
		self.name = name
		self.schema = schema
		self.path = path

AVAILABLE_TOPICS = [
	Topic("odom_zed",     Topic.ODOM,  "/zed/zed_node/odom"),
	Topic("cam_zed_l",    Topic.IMG,   "/zed/zed_node/left_raw/image_raw_color/compressed"),
	Topic("cam_zed_r",    Topic.IMG,   "/zed/zed_node/right_raw/image_raw_color/compressed"),
	Topic("cam_side_l",   Topic.IMG,   "/camera/side_left/image_raw/compressed"),
	Topic("cam_side_r",   Topic.IMG,   "/camera/side_right/image_raw/compressed"),
	Topic("cam_rear_l",   Topic.IMG,   "/camera/rear_left/image_raw/compressed"),
	Topic("cam_rear_r",   Topic.IMG,   "/camera/rear_right/image_raw/compressed"),
	Topic("cam_rear_m",   Topic.IMG,   "/camera/rear_mid/image_raw/compressed"),
	Topic("lidar_ouster", Topic.LIDAR, "/ouster/points")
]

TOPIC_PATHS = set([t.path for t in AVAILABLE_TOPICS])

TOPIC_NAME_LOOKUP = dict()
for t in AVAILABLE_TOPICS:
	TOPIC_NAME_LOOKUP[t.path] = t.name



def main():
	odom_entries = []
	image_index = dict()	# Keep track of current index for each image topic

	os.mkdir(OUT_DIR)

	with open(sys.argv[1], "rb") as f:
		reader = make_reader(f, decoder_factories=[DecoderFactory()])
		for schema, channel, message, ros_msg in reader.iter_decoded_messages(topics=TOPIC_PATHS, start_time=START_TIME, end_time=END_TIME):
			#print(f"{channel.topic} {schema.name} [{message.log_time}]: {ros_msg}")
			# Look up alias for path
			if channel.topic in TOPIC_NAME_LOOKUP:
				topic_alias = TOPIC_NAME_LOOKUP[channel.topic]
			else:
				continue
			# Export method depends on schema
			if schema.name == Topic.ODOM and topic_alias == "zed_odom":
				pose = ros_msg.pose.pose
				pos = pose.position
				rot = pose.orientation
				odom_entries.append({
					"time": message.log_time,
					"pos": {
						"x": pos.x,
						"y": pos.y,
						"z": pos.z
					},
					"rot": {
						"x": rot.x,
						"y": rot.y,
						"z": rot.z,
						"w": rot.w
					}
				})
			elif schema.name == Topic.IMG:
				# Get counter
				if topic_alias not in image_index:
					image_index[topic_alias] = 0
				with open(f"{OUT_DIR}\\{topic_alias}-{image_index[topic_alias]:04}.jpg", "wb") as image_file:
					image_file.write(ros_msg.data)
				image_index[topic_alias] += 1
			elif schema.name == Topic.LIDAR:
				# Get image size
				width = ros_msg.width
				height = ros_msg.height
				pixel_count = width * height
				# Todo: Offsets might differ -> Read from ros_msg.fields
				data = ros_msg.data
				bytes_per_pixel = int(len(data) / pixel_count)

				depth_array = []
				pixel = 0
				while pixel < pixel_count:
					offset = bytes_per_pixel * pixel
					pos_bytes = data[offset:offset+12]
					[x,y,z] = unpack("3f", bytearray(pos_bytes))
					depth_array.append(sqrt(x*x + y*y + z*z) / 40)
					pixel += 1

				# Convert to numpy array
				arr = np.array(depth_array, dtype="float32")
				arr.shape = (height, width)
				imageio.imwrite(f"{OUT_DIR}\\{topic_alias}@{message.log_time}.exr", arr, flags=5) # EXR_FLOAT | EXR_ZIP
	
		# Write accumulated odometry data
		with open(f"{OUT_DIR}\\odom.json", "w") as json_file:
			json_file.write(json.dumps({"odom": odom_entries}, separators=(",",":")))


if __name__ == "__main__":
	main()