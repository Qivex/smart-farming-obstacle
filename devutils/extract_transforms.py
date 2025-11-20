from sys import argv
from os.path import exists
from json import dumps

from mcap.reader import make_reader
from mcap_ros2.decoder import DecoderFactory


def group_by_parent(elems):
	result = {}
	for el in elems:
		parent_id = el["parentID"]
		if parent_id not in result:
			result[parent_id] = []
		del el["parentID"]
		result[parent_id].append(el)
	return result


def construct_node_tree(available_nodes, current_parent_id):
	result = []
	for elem in available_nodes[current_parent_id]:
		if elem["id"] in available_nodes:	# Key exists only if this element has children
			elem["children"] = construct_node_tree(available_nodes, elem["id"])
		result.append(elem)
	return result


def main(argv):
	if len(argv) != 2:
		print(f"Usage: {argv[0]} [rosbag]")
		return

	recording_path = argv[1]

	if not exists(recording_path):
		print("No file at given path!")
		return
	
	file_index = 0
	with open(recording_path, "rb") as recording_file:
		reader = make_reader(recording_file, decoder_factories=[DecoderFactory()])
		for schema, channel, message, ros_msg in reader.iter_decoded_messages(topics=["/tf_static"]):
			included_transforms = []
			potential_root_ids = set()
			for tf in ros_msg.transforms:
				# Shortcuts
				tl = tf.transform.translation
				ro = tf.transform.rotation

				included_transforms.append({
					"id": tf.child_frame_id,
					"parentID": tf.header.frame_id,
					"offset": {"x": tl.x, "y": tl.y, "z": tl.z},
					"childRotation": {"x": ro.x, "y": ro.y, "z": ro.z, "w": ro.w}
				})

				potential_root_ids.add(tf.header.frame_id)

			for tf in included_transforms:
				if tf["id"] in potential_root_ids:
					potential_root_ids.remove(tf["id"])

			children = group_by_parent(included_transforms)
			if len(potential_root_ids) == 1:
				root = potential_root_ids.pop()
				bone_tree = construct_node_tree(children, root)
				with open(f"transforms_{root}.json", "w") as output_file:
					output_file.write(dumps(bone_tree))
				file_index += 1
			else:
				print(potential_root_ids)	# Should never happen


if __name__ == "__main__":
	main(argv)