import bpy


class KeyframeGenerator:
	def __init__(self, interpolator, bone_mapping):
		self.interpolator = interpolator
		self.bone_mapping = bone_mapping
	
	def create_animation(self, armature, timestamps):
		# Pose bones only exist in pose mode
		bpy.context.view_layer.objects.active = armature	# Active armature object required for pose mode
		bpy.ops.object.mode_set(mode='POSE')
		bones = armature.pose.bones

		# Generate required data
		data = self.interpolator.interpolate_values(timestamps)

		# Insert keyframes for each frame
		for current_frame in range(len(timestamps)):
			for entry in self.bone_mapping:
				# Get value
				target_value = data[entry["valueKey"]][current_frame]

				# Get target attribute
				target_info = entry["animationTarget"]
				bone = bones[target_info["boneID"]]
				target_attribute = getattr(bone, target_info["dataPath"])

				# Different rotation mode
				if target_info["dataPath"] == "rotation_euler":
					bone.rotation_mode = "XYZ"

				# Set value using data
				if "dataIndex" in target_info:	# Index argument is required when animating array values
					target_attribute[target_info["dataIndex"]] = target_value
				else:
					target_attribute = target_value

				# Insert keyframe to store state
				bone.keyframe_insert(data_path=target_info["dataPath"], frame=current_frame + 1)	# Blender animations start at frame 1




