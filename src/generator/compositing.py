import bpy


def setup_compositor(scene):
	# Required for scene.node_tree to exist
	scene.use_nodes = True

	# Shortcuts
	nodes = scene.node_tree.nodes
	links = scene.node_tree.links

	# Clear default
	nodes.clear()

	# Create nodes (using bl_idname)
	movie_node  = nodes.new("CompositorNodeMovieClip")
	render_node = nodes.new("CompositorNodeRLayers")
	comp_node   = nodes.new("CompositorNodeComposite")
	alpha_node  = nodes.new("CompositorNodeAlphaOver")
	scale_node  = nodes.new("CompositorNodeScale")

	# Configure nodes
	scale_node.space = "RENDER_SIZE"
	# Note: movie_node.clip is different for each camera (and therefore not set here)

	# Connect nodes
	links.new(movie_node.outputs[0], scale_node.inputs[0])
	links.new(scale_node.outputs[0], alpha_node.inputs[1])
	links.new(render_node.outputs[0], alpha_node.inputs[2])
	links.new(alpha_node.outputs[0], comp_node.inputs[0])

	# Actually use the compositing nodes during render
	scene.render.film_transparent = True
	scene.render.use_compositing = True


def setup_depth_compositor():
	pass


def add_alpha_output_to_compositor():
	pass