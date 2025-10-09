from core import load_config
from schema import extractor_config_schema


def main():
	config = load_config(schema=extractor_config_schema)
	# Check config content for additional details not verifiable with schema
	print(config["rosbagPath"])
	

if __name__ == "__main__":
	main()