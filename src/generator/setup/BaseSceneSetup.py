from . import SceneSetup
from common.const import PANORAMA_SENSOR_PARTITION_AMOUNT
from generator.armature import create_armature
from generator.camera import create_camera


class BaseSceneSetup(SceneSetup):
	def setup(self, config):
		scene = self.scene

		# Render Settings
		scene.render.engine = "CYCLES"	# Required for shadows
		scene.cycles.device = config["render"]["device"]
		scene.cycles.samples = config["render"]["samples"]

		# Construct bone tree
		armature = create_armature(config["bones"])	# Note: Can't store reference to armature because it will break after FULL_COPY

		# Add all sensors
		for sensor in config["sensors"]:
			sensor_type = sensor["type"]
			if sensor_type == "camera":
				create_camera(armature, sensor)
			elif sensor_type == "lidar":
				pass
