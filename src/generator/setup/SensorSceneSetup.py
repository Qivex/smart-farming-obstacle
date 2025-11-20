import bpy

from . import SceneSetup

class SensorSceneSetup(SceneSetup):
	def setup(self, config):
		# From config
		image_root = config["root"]
		sensor_path = config["img"]
		sensor_id = config["id"]

		self.set_image_source(f"{image_root}/{sensor_path}")
		
		for object in self.scene.objects:
			# Set active camera
			if object.type == "CAMERA" and object.name.startswith(sensor_id):
				self.scene.camera = object
			# Add animation to armature
			if object.type == "ARMATURE":
				armature = object
				# TODO
		

	def set_image_source(self, path):
		# Load image source as movie clip
		movie_clip = bpy.data.movieclips.load(path)
		# Set as node value in compositing
		self.scene.node_tree.nodes.get("Movie Clip").clip = movie_clip
		# Match viewport size
		self.scene.render.resolution_x, self.scene.render.resolution_y = movie_clip.size
		# Match scene duration
		self.scene.frame_end = movie_clip.frame_duration
		
		