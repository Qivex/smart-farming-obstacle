from os.path import join

import bpy

from common import load_json
from common.const import IMAGE_FILE_FORMATSTRING, IMAGE_FILE_PART_FORMATSTRING
from generator.camera import create_camera
from . import SceneSetup


class SensorSceneSetup(SceneSetup):
	def setup(self, config):
		# From config
		sensor_config = config["sensor"]
		image_root = config["root"]
		keyframe_generator = config["keyframes"]

		# Set path to images
		sensor_id = sensor_config["id"]
		if sensor_config["type"] == "camera":
			sensor_image_file = IMAGE_FILE_FORMATSTRING.format(id=sensor_id, index=1, format="jpg")
		elif sensor_config["type"] == "lidar":
			sensor_image_file = IMAGE_FILE_PART_FORMATSTRING.format(id=sensor_id, index=1, part=config["part"] or 0, format="exr")
		self.set_image_source(join(image_root, sensor_id, sensor_image_file))

		# Find armature
		for object in self.scene.objects:
			if object.type == "ARMATURE":
				armature = object
		
		# Add animation to armature
		timestamps = load_json(join(image_root, sensor_id, "timeinfo.json"), "timestamps")
		keyframe_generator.create_animation(armature, timestamps)

		# Create camera for scene
		self.scene.camera = create_camera(armature, sensor_config)
		

	def set_image_source(self, path):
		# Load image source as movie clip
		movie_clip = bpy.data.movieclips.load(path)
		# Set as node value in compositing
		self.scene.node_tree.nodes.get("Movie Clip").clip = movie_clip
		# Match viewport size
		self.scene.render.resolution_x, self.scene.render.resolution_y = movie_clip.size
		# Match scene duration
		self.scene.frame_end = movie_clip.frame_duration
		