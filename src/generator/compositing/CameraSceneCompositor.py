from . import SceneCompositor

class CameraSceneCompositor(SceneCompositor):
	def setup(self):
		nodes = self.nodes
		links = self.links

		# Create nodes
		movie_node  = nodes.new("CompositorNodeMovieClip")
		render_node = nodes.new("CompositorNodeRLayers")
		alpha_node  = nodes.new("CompositorNodeAlphaOver")
		out_node    = nodes.new("CompositorNodeComposite")

		# Connect nodes
		links.new( movie_node.outputs[0], alpha_node.inputs[1])
		links.new(render_node.outputs[0], alpha_node.inputs[2])
		links.new( alpha_node.outputs[0],   out_node.inputs[0])

		# Reference required when using alpha mask
		self.render_node = render_node
