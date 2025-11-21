import bpy
from abc import ABC, abstractmethod

# TODO: Use bpy.context.collection.all_objects to get objects of current scene only

class SceneSetup(ABC):
	@abstractmethod
	def setup(self, config):
		pass


	def create_scene(self, parent_scene, scene_name, config=None):
		# Activate parent scene (because operator always applies to active scene)
		bpy.context.window.scene = parent_scene

		# Create new scene by copying from an existing scene
		bpy.ops.scene.new(type="FULL_COPY")	# This also activates the newly created scene
		self.scene = bpy.context.scene
		self.scene.name = scene_name

		# Execute concrete setup implementation
		self.setup(config)

		# Set scene to object mode
		bpy.ops.object.mode_set(mode="OBJECT")

		# Return created scene
		return self.scene