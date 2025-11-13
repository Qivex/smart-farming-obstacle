from abc import ABC, abstractmethod

class SceneCompositor(ABC):
	def __init__(self, scene, enable_alpha_mask_generation=False):
		scene.use_nodes = True	# Required for scene.node_tree to exist

		# Shortcuts
		self.scene = scene
		self.nodes = scene.node_tree.nodes
		self.links = scene.node_tree.links

		# Clear default
		self.nodes.clear()

		# Call concrete implementations
		self.setup()
		if enable_alpha_mask_generation == True:
			self.setup_alpha()
		
		# Enable created compositing logic
		scene.render.use_compositing = True


	def setup_alpha(self):
		# Shortcuts
		nodes = self.nodes
		links = self.links
		render_node = self.render_node
		scene_name = self.scene.name

		# Create required nodes
		combine_node = nodes.new("CompositorNodeCombineColor")
		file_node    = nodes.new("CompositorNodeOutputFile")

		# Define file output
		file_node.base_path = f"//alpha\\{scene_name}"	# Additional folder for alpha mask output
		file_node.file_slots[0].path = f"{scene_name}-"
		file_node.format.file_format = "PNG"
		file_node.format.compression = 100
		file_node.format.color_mode = "BW"

		# Map render alpha to each RGB channel
		for i in range(3):
			links.new(render_node.outputs[1], combine_node.inputs[i])
		links.new(combine_node.outputs[0], file_node.inputs[0])


	@abstractmethod
	def setup(self):
		pass