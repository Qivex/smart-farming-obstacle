from math import pi

import bpy


def create_camera(armature, config):
	# Create camera object
	bpy.ops.object.mode_set(mode="OBJECT")
	bpy.ops.object.camera_add()
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
	# Fix camera to bone head...
	target_bone_name = config["parentBone"]
	location_constraint = camera.constraints.new("COPY_LOCATION")
	location_constraint.target = armature
	location_constraint.subtarget = target_bone_name
	# ... and track tail
	tracking_constraint = camera.constraints.new("TRACK_TO")
	tracking_constraint.target = armature
	tracking_constraint.subtarget = target_bone_name
	tracking_constraint.head_tail = 1	# Tail
	return camera