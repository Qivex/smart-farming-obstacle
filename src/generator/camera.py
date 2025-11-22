from math import pi

import bpy

from common.const import PANORAMA_SENSOR_PARTITION_AMOUNT


def _rotate(vector, axis, angle):
	pass


def create_camera(armature, config, part=0):
	bpy.ops.object.mode_set(mode="OBJECT")
	# Calculate initial rotation

	#if config["type"] == "camera":
	r = config["rotationEuler"]
	initial_rotation = (r["x"], r["y"], r["z"])
	#elif config["type"] == "lidar":
	# r = config["rotationAxis"]
	# rotation_axis = Vector(r["x"], r["y"], r["z"])
	# default_first = rotation_axis.orthogonal()
	# initial_rotation = _rotate(default_first, axis, config["firstAngle"] + (360 / PANORAMA_SENSOR_PARTITION_AMOUNT) * part)
	# Create camera object
	bpy.ops.object.camera_add(rotation=initial_rotation)
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
	# Attach camera to bone
	target_bone = config["parentBone"]
	location_constraint = camera.constraints.new("COPY_LOCATION")
	location_constraint.target = armature
	location_constraint.subtarget = target_bone
	location_constraint.head_tail = 1	# Follow tail
	rotation_constraint = camera.constraints.new("COPY_ROTATION")
	rotation_constraint.target = armature
	rotation_constraint.subtarget = target_bone
	rotation_constraint.mix_mode = "ADD"	# Add initial rotation to current
	return camera