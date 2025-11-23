from math import pi

import bpy
from mathutils import Matrix

from common.const import PANORAMA_SENSOR_PARTITION_AMOUNT


def create_camera(armature, config, part=0):
	bpy.ops.object.mode_set(mode="OBJECT")

	# Create camera object
	r = config["rotationEuler"]
	bpy.ops.object.camera_add(rotation=(r["x"], r["y"], r["z"]))
	camera = bpy.context.active_object

	# Apply additional rotation proportional to current part
	if config["type"] == "lidar":
		angle = 2*pi*part / PANORAMA_SENSOR_PARTITION_AMOUNT
		bpy.ops.transform.rotate(value=angle, orient_type="LOCAL", orient_axis="Y", orient_matrix_type="LOCAL", orient_matrix=Matrix.Identity(3))
		# This looks simple, but imagine how complex this calculation is without local transformation orientation...

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
	rotation_constraint.mix_mode = "BEFORE"	# Apply own rotation first

	return camera