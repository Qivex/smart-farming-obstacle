from . import SceneSetup
from generator.armature import create_armature


class BaseSceneSetup(SceneSetup):
	def setup(self, config):
		scene = self.scene

		# Render Settings
		scene.render.engine = "CYCLES"	# Required for shadows
		scene.cycles.device = config["render"]["device"]
		scene.cycles.samples = config["render"]["samples"]

		# Construct bone tree
		create_armature(config["bones"])	# Note: Can't store reference to armature because it will break after FULL_COPY
