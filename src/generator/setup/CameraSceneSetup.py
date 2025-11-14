import bpy

from . import SceneSetup
from generator.compositing import CameraSceneCompositor


def create_shadow_catcher(obstacle_id):
	# Find obstacle
	try:
		obstacle_object = bpy.data.objects[obstacle_id]
	except KeyError:
		print(f"Obstacle with id {obstacle_id} was not found in provided scene!")

	# Create primitve plane below obstacle object
	width, depth, height = obstacle_object.dimensions
	shadow_size = max(width, depth) + 10 * height
	lowest_point = obstacle_object.location.z - height / 2
	bpy.ops.mesh.primitive_plane_add(size=shadow_size, location=(0, 0, lowest_point))

	# Make shadow catcher
	shadow_catcher = bpy.context.active_object
	shadow_catcher.is_shadow_catcher = True


class CameraSceneSetup(SceneSetup):
	def setup(self, config):
		CameraSceneCompositor(self.scene, config["output"]["generateAlphaMaps"])
		create_shadow_catcher(config["scene"]["obstacleID"])
	