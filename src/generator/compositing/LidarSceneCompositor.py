'''
Because the Lidar sensor outputs a full 360° panoramic image, several cameras are required to render the entire visible area.
The output however should still be a single panoramic image instead of multiple rendered images each containing just a subsection.

The composite of each rendered subsection can be combined into a single output by creating an additional scene:
https://blender.stackexchange.com/a/150113
https://blender.stackexchange.com/q/315035

The compositing logic required for this additonal abstract scene is contained in this script.
'''

import bpy

from core.const import VIEWPORT_CLIP_NEAR, VIEWPORT_CLIP_FAR
from . import SceneCompositor


# TODO: Combine multiple scenes f"${scene_name}_part{i}" into a single panorama output before comp with movieclip
PANORAMA_SENSOR_PARTITION_AMOUNT = 3


class LidarSceneCompositor(SceneCompositor):
	def setup(self):
		# Shortcuts
		nodes = self.nodes
		links = self.links
		scene_name = self.scene.name

		# Unique elements
		movie_node = nodes.new("CompositorNodeMovieClip")
		combine_node = nodes.new("CompositorNodeZcombine")
		out_node = nodes.new("CompositorNodeComposite")
		file_node = nodes.new("CompositorNodeOutputFile")
		split_node1 = nodes.new("CompositorNodeSplit")
		split_node2 = nodes.new("CompositorNodeSplit")

		combine_node.inputs[1].default_value = 0	# Always prefer render depth (if available)
		combine_node.inputs[5].default_value = False	# Disable Anti-Aliasing

		links.new(split_node1.outputs[0], split_node2.inputs[1])
		links.new(split_node2.outputs[0], out_node.inputs[0])

		file_node.base_path = f"d:\\alpha\\{scene_name}"	# Additional folder for alpha mask output
		file_node.file_slots[0].path = f"{scene_name}-"
		file_node.format.file_format = "PNG"
		file_node.format.compression = 100
		file_node.format.color_mode = "BW"
		file_node.save_as_render = True

		possible_inputs = [
			split_node1.inputs[1],
			split_node1.inputs[2],
			split_node2.inputs[2]
		]


		# Required for each section
		for i in range(PANORAMA_SENSOR_PARTITION_AMOUNT):
			# Ensure each of the required subsections scenes exist
			section_scene = bpy.data.scenes.get(f"{scene_name}_part{i}")
			if section_scene is None:
				raise NameError(f"Scene {i} of panorama {scene_name} was not found!")
			
			# Required for output "Depth" to exist on node "Render Layers"
			section_scene.view_layers["ViewLayer"].use_pass_z = True

			# Create nodes
			render_node  = nodes.new("CompositorNodeRLayers")
			scale_node   = nodes.new("CompositorNodeScale")
			map_node     = nodes.new("ShaderNodeMapRange")
			# mix_node = nodes.new()	# TEMP

			# Set composite of each subsection as source
			render_node.scene = section_scene

			# Don't stretch to full panorama width
			scale_node.space = "RENDER_SIZE"

			# Map viewport depth to float [0..1]
			map_node.inputs[1].default_value = VIEWPORT_CLIP_NEAR
			map_node.inputs[2].default_value = VIEWPORT_CLIP_FAR

			# Connect nodes
			links.new(render_node.outputs[2], scale_node.inputs[0])
			links.new(scale_node.outputs[0], map_node.inputs[0])
			links.new(map_node.outputs[0], possible_inputs[i])

			

		
		

		
		'''
		# Create nodes
		movie_node   = nodes.new("CompositorNodeMovieClip")
		crop_node    = nodes.new("CompositorNodeCrop")
		
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

	'''
		# Reference required when setting movie clip
		self.movie_node = movie_node
	

	def set_movie_clip(self, movie_clip):
		self.movie_node.clip = movie_clip
