from struct import unpack
from math import sqrt

import numpy as np
import imageio
imageio.plugins.freeimage.download()	# Required for OpenEXR

from . import ImageTopicExtractor
from core.const import VIEWPORT_CLIP_NEAR, VIEWPORT_CLIP_FAR



def _clip_depth(value, near, far):
	if value > far:
		return 1
	if value < near:
		return 0
	return (value - near) / (far - near)


class LidarImageTopicExtractor(ImageTopicExtractor):
	def __init__(self, id, export_root):
		super().__init__(id, export_root)


	def on_message(self, message):
		self.append_timestamp(message.stamp)

		# Get image size
		width = message.width
		height = message.height
		pixel_count = width * height

		# Calculcate bytes-per-pixel-constant
		data = message.data
		bpp = int(len(data) / pixel_count)

		# Calculate depth value for each pixel from point cloud
		clipped_depth_values = []
		pixel = 0
		while pixel < pixel_count:
			offset = bpp * pixel
			# Important: Offsets might differ -> See message.fields
			pos_bytes = data[offset:offset+12]
			[x,y,z] = unpack("3f", bytearray(pos_bytes))
			depth = sqrt(x*x + y*y + z*z)
			clipped_depth_values.append(_clip_depth(depth, VIEWPORT_CLIP_NEAR, VIEWPORT_CLIP_FAR))
			pixel += 1

		# Convert to numpy array
		arr = np.array(clipped_depth_values, dtype="float32")
		arr.shape = (height, width)

		# Write image to folder
		imageio.imwrite(self.get_image_path("exr"), arr, flags=5)	# From FreeImage.h: EXR_FLOAT = 1, EXR_ZIP = 4
		