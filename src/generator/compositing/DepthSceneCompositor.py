import bpy

from core.const import VIEWPORT_CLIP_NEAR, VIEWPORT_CLIP_FAR
from . import SceneCompositor


# TODO: Combine multiple scenes f"${scene_name}_part{i}" into a single panorama output before comp with movieclip
PANORAMA_SENSOR_PARTITION_AMOUNT = 3


class DepthSceneCompositor(SceneCompositor):
	def setup(self):
		nodes = self.nodes
		links = self.links
		scene_name = self.scene.name

		# Required for output "Depth" to exist on node "Render Layers"
		self.scene.view_layers["ViewLayer"].use_pass_z = True

		# Create nodes
		movie_node   = nodes.new("CompositorNodeMovieClip")
		crop_node    = nodes.new("CompositorNodeCrop")
		render_node  = nodes.new("CompositorNodeRLayers")
		math_node    = nodes.new("ShaderNodeMath")
		map_node     = nodes.new("ShaderNodeMapRange")
		combine_node = nodes.new("CompositorNodeZcombine")
		out_node     = nodes.new("CompositorNodeComposite")

		# Invert render alpha
		math_node.operation = "SUBTRACT"
		math_node.inputs[0].default_value = 1

		# Map viewport depth to float [0..1]
		map_node.inputs[1].default_value = VIEWPORT_CLIP_NEAR
		map_node.inputs[2].default_value = VIEWPORT_CLIP_FAR

		# Configure z combine
		combine_node.inputs[1].default_value = 0	# Always prefer render depth (if available)
		combine_node.inputs[5].default_value = False	# Disable Anti-Aliasing

		# Connect nodes
		links.new( render_node.outputs[1],    math_node.inputs[1])
		links.new(   math_node.outputs[0], combine_node.inputs[3])
		links.new( render_node.outputs[2],     map_node.inputs[0])	# Requires use_pass_z
		links.new(    map_node.outputs[0], combine_node.inputs[2])
		links.new(  movie_node.outputs[0],    crop_node.inputs[0])	# See note below
		links.new(   crop_node.outputs[0], combine_node.inputs[0])
		links.new(combine_node.outputs[0],     out_node.inputs[0])

		# Note: Crop node no longer supports relative values!
		# https://docs.blender.org/manual/en/4.4/compositing/types/transform/crop.html
		# https://docs.blender.org/manual/en/4.5/compositing/types/transform/crop.html
		# => Absolute values must be set when selecting movie clip!!

		# Reference required when using alpha mask
		self.render_node = render_node

		# Reference required when setting movie clip
		self.movie_node = movie_node
		self.crop_node = crop_node
	

	def set_movie_clip(self, movie_clip):
		self.movie_node.clip = movie_clip

		# Update panorama crop
		crop = self.crop_node
		size = movie_clip.size
		crop.inputs[0].default_value = size[0] * part_index
