from math import floor
from os import makedirs
from os.path import isfile, realpath
from sys import exit
from time import time

from mcap.reader import make_reader
from mcap_ros2.decoder import DecoderFactory

from core import load_config
from extractor import TopicExtractorFactory
from schema import extractor_config_schema



def main():
	config = load_config(schema=extractor_config_schema)

	# Read values from config
	start_time = config["startTime"] * 1e9 if "startTime" in config else None
	end_time   = config["endTime"]   * 1e9 if "endTime"   in config else None
	try:
		recording_path = realpath(config["recordingPath"], strict=True)
	except FileNotFoundError as e:
		print(f"No recording file found at:\n\t{recording_path}")
		exit()
	except Exception as e:
		print(f"Unknown error when trying to access recording file:\n\t{e}")

	# Create export directory
	try:
		export_path = f"{realpath(config['exportPath'])}@{floor(time())}"	# Add timestamp to avoid overwriting previous export
		makedirs(export_path)
	except Exception as e:
		print(f"Error while creating output directory:\n\t{e}")
	
	# Init topic extractors
	topic_extractors = {}
	topic_extractor_factory = TopicExtractorFactory(export_path)
	for topic_config in config["topics"]:
		path = topic_config["path"]
		extractor = topic_extractor_factory.create_from_config(topic_config)
		extractor.before_extract()
		topic_extractors[path] = extractor
		
	# Iterate through messages
	with open(recording_path, "rb") as recording_file:
		reader = make_reader(recording_file, decoder_factories=[DecoderFactory()])
		for schema, channel, message, ros_msg in reader.iter_decoded_messages(topics=topic_extractors.keys(), start_time=start_time, end_time=end_time):
			# Execute assigned extractor
			if channel.topic in topic_extractors:
				extractor = topic_extractors[channel.topic]
				extractor.on_message(ros_msg, message.publish_time)

	# Close extractors
	for extractor in topic_extractors.values():
		extractor.after_extract()
	

if __name__ == "__main__":
	main()