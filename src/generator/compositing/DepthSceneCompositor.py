import bpy

from common.const import VIEWPORT_CLIP_NEAR, VIEWPORT_CLIP_FAR
from . import SceneCompositor


class DepthSceneCompositor(SceneCompositor):
	def setup(self):
		nodes = self.nodes
		links = self.links

		# Required for output "Depth" to exist on node "Render Layers"
		self.scene.view_layers["ViewLayer"].use_pass_z = True

		# Create nodes
		movie_node   = nodes.new("CompositorNodeMovieClip")
		render_node  = nodes.new("CompositorNodeRLayers")
		math_node    = nodes.new("ShaderNodeMath")
		map_node     = nodes.new("ShaderNodeMapRange")
		combine_node = nodes.new("CompositorNodeZcombine")
		file_node    = nodes.new("CompositorNodeOutputFile")

		# Invert render alpha
		math_node.operation = "SUBTRACT"
		math_node.inputs[0].default_value = 1

		# Map viewport depth to float [0..1]
		map_node.inputs[1].default_value = VIEWPORT_CLIP_NEAR
		map_node.inputs[2].default_value = VIEWPORT_CLIP_FAR

		# Configure z combine
		combine_node.inputs[1].default_value = 0	# Always prefer depth value from render (if available)
		combine_node.inputs[5].default_value = False	# Disable Anti-Aliasing

		# Configure File output
		file_node.name = "Output"
		file_node.format.file_format = "OPEN_EXR"
		file_node.format.exr_codec = "ZIP"
		file_node.format.color_depth = "32"

		# Connect nodes
		links.new( render_node.outputs[1],    math_node.inputs[1])
		links.new(   math_node.outputs[0], combine_node.inputs[3])
		links.new( render_node.outputs[2],     map_node.inputs[0])	# Requires use_pass_z
		links.new(    map_node.outputs[0], combine_node.inputs[2])
		links.new(  movie_node.outputs[0], combine_node.inputs[0])
		links.new(combine_node.outputs[0],     file_node.inputs[0])

		# Reference required when using alpha mask
		self.render_node = render_node
