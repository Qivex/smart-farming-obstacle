import bpy
from mathutils import Vector, Quaternion


def _create_bone(edit_bones, data, parent_bone, parent_rotation=Quaternion((1,0,0,0)), parent_is_root=False):
	bone = edit_bones.new(data["id"])
	# Connect to parent
	bone.parent = parent_bone
	# Define head position
	if parent_is_root:
		bone.use_connect = False
		bone.head = parent_bone.head
	else:
		bone.use_connect = True	# Implicitly connects bone.head with parent_bone.tail
	# Temporary vector to calculate bone head
	o = data["offset"]	# Shortcut
	offset = Vector((o["x"], o["y"], o["z"]))
	offset.rotate(parent_rotation)	# Apply cumulative rotations (of all previous transform frames)
	# Tail position relative to head
	head = bone.head
	bone.tail = (
		head[0] + offset[0],
		head[1] + offset[1],
		head[2] + offset[2]
	)
	if "children" in data:
		# Add own rotation to cumulative rotation of all parents
		r = data["childRotation"]	# Shortcut
		child_rotation = Quaternion((r["w"], r["x"], r["y"], r["z"]))
		child_rotation.rotate(parent_rotation)
		# Create all child bones recursively
		for child_data in data["children"]:
			_create_bone(edit_bones, child_data, bone, child_rotation)


def create_armature(bone_config):
	# Init default armature
	bpy.ops.object.armature_add(enter_editmode=True)
	armature = bpy.context.active_object
	edit_bones = armature.data.edit_bones
	# Remove default bone
	edit_bones.remove(edit_bones.get("Bone"))
	# Create root bone
	root_bone = edit_bones.new("root")
	root_bone.head = (0,0,0)
	root_bone.tail = (0,0,1)
	# Create bone tree from config
	for bone_data in bone_config:
		_create_bone(edit_bones, bone_data, root_bone, parent_is_root=True)
	return armature