from . import SceneCompositor

class CameraSceneCompositor(SceneCompositor):
	def setup(self):
		nodes = self.nodes
		links = self.links

		# Create nodes
		movie_node   = nodes.new("CompositorNodeMovieClip")
		render_node  = nodes.new("CompositorNodeRLayers")
		balance_node = nodes.new("CompositorNodeColorBalance")
		alpha_node   = nodes.new("CompositorNodeAlphaOver")
		file_node    = nodes.new("CompositorNodeOutputFile")

		# Configure File output
		file_node.name = "Output"
		file_node.format.file_format = "PNG"
		file_node.format.compression = 100

		# Connect nodes
		links.new(  movie_node.outputs[0],   alpha_node.inputs[1])
		links.new( render_node.outputs[0], balance_node.inputs[1])
		links.new( render_node.outputs[1], balance_node.inputs[0])
		links.new(balance_node.outputs[0],	 alpha_node.inputs[2])
		links.new(  alpha_node.outputs[0],    file_node.inputs[0])

		# Reference required when using alpha mask
		self.render_node = render_node

		# Reference required to set lift of color balance
		self.balance_node = balance_node
	
	def set_lift(self, lift):
		self.balance_node.inputs[2].default_value = lift
