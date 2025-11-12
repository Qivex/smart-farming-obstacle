import bpy

def create_animation2(armature, data_mapping, tracking_data):
	# Pose bones only exist in pose mode
	bpy.ops.object.mode_set(mode='POSE')
	bones = armature.pose.bones

	# Insert keyframes for each frame
	for current_frame, data in enumerate(tracking_data):
		# Apply all values of a single frame according to the data mapping
		for pair in data_mapping:
			source_path = pair["odomSource"]
			target_info = pair["animTarget"]
			
			# Find targeted bone & its attribute
			bone_id = target_info["boneID"]
			bone = bones[bone_id]
			target_attribute = getattr(bone, target_info["dataPath"])

			# Resolve JSON path in data
			target_value = data
			for key in source_path:
				target_value = target_value[key]

			# Set value using data
			if "dataIndex" in target_info:	# Index argument is required when animating array values
				target_attribute[target_info["dataIndex"]] = target_value
			else:
				target_attribute = target_value

			# Insert keyframe to store state
			bone.keyframe_insert(data_path=target_info["dataPath"], frame=current_frame + 1)	# Blender animations start at frame 1



def create_animation(armature, data_mapping, tracking_data):
	# Boilerplate for Blender animation (https://docs.blender.org/api/current/info_quickstart.html#animation)
	action = bpy.data.actions.new(name="ProceduralAnimationFromTracking")
	slot = action.slots.new(armature.id_type, armature.name)
	layer = action.layers.new("Layer")
	strip = layer.strips.new(type="KEYFRAME")
	channelbag = strip.channelbag(slot, ensure=True)
	fcurves = channelbag.fcurves

	# Assign animation data using the data mapping (source from odometry -> target in animation)
	for pair in data_mapping:
		target = pair["animTarget"]

		# Create fcurve (= all keyframes for a single value)
		bone = target["boneID"]
		path = target["dataPath"]
		full_data_path = f'pose.bones["{bone}"].{path}'
		if "dataIndex" in target:	# Index argument is required when animating array values
			fcurve = fcurves.new(data_path=full_data_path, index=target["dataIndex"])
		else:
			fcurve = fcurves.new(data_path=full_data_path)
		keyframes = fcurve.keyframe_points

		# Insert all available data points (tracking_data is already transformed & interpolated)
		for current_frame, datapoint in enumerate(tracking_data):
			# Resolve path in JSON to access value
			jsonPath = pair["odomSource"]
			value = datapoint
			for key in jsonPath:
				value = value[key]
			# Append to keyframes
			keyframes.insert(frame=current_frame, value=value)

	# Use created action as animation for armature
	animation = armature.animation_data_create()
	animation.action = action
	animation.action_slot = slot
