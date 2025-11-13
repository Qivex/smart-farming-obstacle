import bpy

from . import Scene
from generator.armature import create_armature


# Scene configuration & Bone Rigging
class BaseScene(Scene):
	def create_shadow_catcher(self, obstacle_id):
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
		return shadow_catcher
	
	def create_armature(self, bone_config):
		return create_armature(bone_config)
