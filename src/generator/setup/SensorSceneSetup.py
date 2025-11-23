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
		sensor_id = sensor_config["id"]
		image_root = config["root"]
		keyframe_generator = config["keyframes"]

		# Set path to images
		if sensor_config["type"] == "camera":
			sensor_image_file = IMAGE_FILE_FORMATSTRING.format(id=sensor_id, index=1, format="jpg")
		elif sensor_config["type"] == "lidar":
			sensor_image_file = IMAGE_FILE_PART_FORMATSTRING.format(id=sensor_id, index=1, part=config["part"] or 0, format="exr")
		
		# Load image source as movie clip
		movie_clip = bpy.data.movieclips.load(join(image_root, sensor_id, sensor_image_file))
		
		# Match viewport size & scene duration
		self.scene.render.resolution_x, self.scene.render.resolution_y = movie_clip.size
		self.scene.frame_end = movie_clip.frame_duration
		
		# Configure nodes
		nodes = self.scene.node_tree.nodes
		for node in nodes:
			if node.bl_idname == "CompositorNodeOutputFile":	# Note: The API for this node has changed in Blender 5.0!!
				# Set output path(s)
				node.file_slots[0].path = f"{self.scene.name}-"
				if node.name.startswith("Output"):
					node.base_path = f"//render\\{sensor_id}"
				elif node.name.startswith("Alpha"):
					node.base_path = f"//alpha\\{sensor_id}"
			elif node.bl_idname == "CompositorNodeMovieClip":
				# Set movie clip for node
				node.clip = movie_clip

		# Find armature
		for object in self.scene.objects:
			if object.type == "ARMATURE":
				armature = object
		
		# Add animation to armature
		timestamps = load_json(join(image_root, sensor_id, "timeinfo.json"), "timestamps")
		keyframe_generator.create_animation(armature, timestamps)

		# Create camera for scene
		if sensor_config["type"] == "camera":
			camera = create_camera(armature, sensor_config)
		elif sensor_config["type"] == "lidar":
			camera = create_camera(armature, sensor_config, part=config["part"])
		self.scene.camera = camera	# Set as active camera for render

		# Camera Background Images
		if bpy.app.background == False:	# Only required for GUI
			camera.data.show_background_images = True
			camera_background_image = camera.data.background_images.new()
			camera_background_image.alpha = 1
			camera_background_image.source = "MOVIE_CLIP"
			camera_background_image.clip = movie_clip


		
		