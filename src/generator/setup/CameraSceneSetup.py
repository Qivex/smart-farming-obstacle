import bpy

from . import SceneSetup
from generator.compositing import CameraSceneCompositor


def create_shadow_catcher(scene, obstacle_id):
	# Find obstacle
	obstacle_object = None
	for object in scene.objects:
		if object.name.startswith(obstacle_id):
			obstacle_object = object
			break
	if obstacle_object is None:
		print(f"Obstacle with id {obstacle_id} was not found in provided scene!")
		return

	# Create primitve plane below obstacle object
	width, depth, height = obstacle_object.dimensions
	if width * depth * height == 0:
		# Fallback for grouped objects (= no dimensions)
		shadow_size = 10
		lowest_point = 0
	else:
		shadow_size = max(width, depth) + 10 * height
		lowest_point = obstacle_object.location.z - height / 2
	bpy.ops.mesh.primitive_plane_add(size=shadow_size, location=(0, 0, lowest_point))

	# Make shadow catcher
	shadow_catcher = bpy.context.active_object
	shadow_catcher.is_shadow_catcher = True


def create_sun(config):
	bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
	sun = bpy.context.active_object
	# Sun orientation
	sun.rotation_mode = "QUATERNION"
	angle = config["angle"]
	sun.rotation_quaternion = (angle["w"], angle["x"], angle["y"], angle["z"])
	# Sun appearance
	sun.data.energy = config["strength"]
	sun.data.use_temperature = True
	sun.data.temperature = config["temperature"]


class CameraSceneSetup(SceneSetup):
	def setup(self, config):
		CameraSceneCompositor(self.scene, config["output"]["generateAlphaMaps"])
		create_shadow_catcher(self.scene, config["scene"]["obstacleID"])
		create_sun(config["scene"]["sun"])
	