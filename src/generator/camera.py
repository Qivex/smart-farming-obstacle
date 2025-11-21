from math import pi

import bpy
from mathutils import Euler, Matrix, Vector


def create_camera(armature, config):
	# Find target bone
	bpy.context.view_layer.objects.active = armature	# Active armature object required for edit mode
	bpy.ops.object.mode_set(mode="EDIT")	# Required because head is always at root in Object Mode
	target_bone = armature.data.edit_bones.get(config["parentBone"])
	head = Vector(target_bone.head)
	tail = Vector(target_bone.tail)
	rotation = Matrix(target_bone.matrix).to_euler("XYZ")	# Rotated down by 90 degrees, but gives correct alignment for tracking
	# Create camera object
	bpy.ops.object.mode_set(mode="OBJECT")
	bpy.ops.object.camera_add(location=head, rotation=rotation)
	camera = bpy.context.active_object
	# Adjust camera data
	camera.name = config["id"]
	camera.data.lens_unit = "FOV"
	fov = config["fov"] / 180 * pi
	camera.data.angle = fov
	if "fisheye" in config:
		camera.data.type = "PANO"	# Requires CYCLES rendering engine
		camera.data.panorama_type = config["fisheye"]["mode"]
		camera.data.fisheye_fov = fov
		if camera.data.panorama_type == "FISHEYE_EQUISOLID":
			camera.data.fisheye_lens = config["fisheye"]["lens"]
	# Target object for tracking fixed at tail
	bpy.ops.object.empty_add(location=tail.to_tuple())
	tracking_target = bpy.context.active_object
	tracking_target.name = f"target_{config['id']}"
	tracking_constraint = tracking_target.constraints.new("COPY_LOCATION")
	tracking_constraint.target = armature
	tracking_constraint.subtarget = config["parentBone"]
	tracking_constraint.head_tail = 1	# Always at Tail
	# Fix camera to bone...
	camera_location_constraint = camera.constraints.new("COPY_LOCATION")
	camera_location_constraint.target = armature
	camera_location_constraint.subtarget = config["parentBone"]
	# ... and track target at tail
	camera_tracking_constraint = camera.constraints.new("TRACK_TO")
	camera_tracking_constraint.target = tracking_target