import bpy


def _create_bone(edit_bones, data, parent, parent_is_root=False):
	bone = edit_bones.new(data["id"])
	# Connect to parent
	bone.parent = parent
	# Define head position
	if parent_is_root:
		bone.use_connect = False
		bone.head = parent.head
	else:
		bone.use_connect = True	# Implicitly connects bone.head with parent.tail
	# Tail position relative to head
	head = bone.head
	offset = data["offset"]
	bone.tail = (
		head[0] + offset["x"],
		head[1] + offset["y"],
		head[2] + offset["z"]
	)
	# Recursive child bones
	if "children" in data:
		for child_data in data["children"]:
			_create_bone(edit_bones, child_data, bone)


def create_armature(bone_config):
	# Init default armature
	bpy.ops.object.armature_add(enter_editmode=True)
	armature = bpy.context.active_object.data
	edit_bones = armature.edit_bones
	# Remove default bone
	edit_bones.remove(edit_bones.get("Bone"))
	# Create root bone
	root_bone = edit_bones.new("root")
	root_bone.head = (0,0,0)
	root_bone.tail = (0,0,1)
	# Create bone tree from config
	for bone_data in bone_config:
		_create_bone(edit_bones, bone_data, root_bone, True)