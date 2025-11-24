# Inform about additonal requirements
from sys import exit

try:
	import torch
except ImportError:
	print("Install additional requirements to execute the validator:")
	print("https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt")
	exit()


# Load config
from common import load_config
from schema import validator_config_schema

config = load_config(schema=validator_config_schema)


# Insprired by https://docs.ultralytics.com/de/yolov5/quickstart_tutorial/#inference-with-pytorch-hub
from PIL import Image

# Load images
images = []
for image_path in config["images"]:
	try:
		images.append(Image.load(image_path))
	except Exception as e:
		print(f"Failed to load image from path {image_path}:\n\t{e}")

# Run inference
model = torch.hub.load("ultralytics/yolov5", config["model"])
results = model(images)
operation = getattr(results, config["method"])
operation()