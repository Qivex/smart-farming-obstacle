import bpy
import json
from math import log10, floor, pi
from os import getcwd, mkdir
from time import time

# Some logic is only required with a GUI
WITH_GUI = False if bpy.app.background else True



##########
# CONFIG #
##########

config = {
	"odom_file": "d:\\Uni\\Bachelorarbeit\\Smart Farming Lab\\Code\\test\\odom.json",
	"cameras": [
		{
			"name": "zed_left",
			"image_path": "d:\\Uni\\Bachelorarbeit\\Smart Farming Lab\\Code\\test\\images-1755074139\\zed_left-0001.jpg"
		}
	]
}



###########
# FOLDERS #
###########

cwd = "d:\\Uni\\Bachelorarbeit\\Smart Farming Lab\\Code\\test" if WITH_GUI else getcwd()
output_dir = f"output-{floor(time())}"
output_path = f'{cwd}\\{output_dir}'

mkdir(output_path)
bpy.ops.wm.save_as_mainfile(filepath=f'{output_path}\\test.blend')	# Required for relative paths




###############
# SCENE RESET #
###############

# Remove all default objects (cube, camera, light)
for object in bpy.data.objects:
	bpy.data.objects.remove(object)

# Remove default collection
for collection in bpy.data.collections:
	bpy.data.collections.remove(collection)

# Replace default scene with a newly created one
default_scene = bpy.context.scene
scene = bpy.data.scenes.new("base_scene")
bpy.data.scenes.remove(default_scene)



###################
# SHARED SETTINGS #
###################

# TEMP Faster render for testing (default 64)
scene.eevee.taa_render_samples = 1

# Preserve original color of source video
scene.view_settings.view_transform = "Standard"

# Output file format
scene.render.image_settings.file_format = "PNG"



############
# OBSTACLE #
############

# Simple cube
bpy.ops.mesh.primitive_cube_add(location=(-1690,851,132), scale=(0.3,0.3,0.3))
mat = bpy.data.materials.new(name="cube_mat")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (1,0,0,1)
bpy.context.active_object.data.materials.append(mat)


# Simple light source
bpy.ops.object.light_add(type="POINT", location=(-1691,850,134))
bpy.context.object.data.energy = 80



###############
# COMPOSITING #
###############

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



#########
# BONES #
#########

bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
armature_object = bpy.context.active_object

# Animation
def add_anim_to_armature(armature):
	# Boilerplate at https://docs.blender.org/api/current/info_quickstart.html#animation
	armature.rotation_mode = "QUATERNION"
	
	action = bpy.data.actions.new(name="OdometryTracking")
	slot = action.slots.new(armature.id_type, armature.name)
	strip = action.layers.new("whydoineedalayer").strips.new(type="KEYFRAME")
	channelbag = strip.channelbag(slot, ensure=True)

	fcurves = channelbag.fcurves
	fcurve_rw = fcurves.new(data_path="rotation_quaternion", index=0)
	fcurve_rx = fcurves.new(data_path="rotation_quaternion", index=1)
	fcurve_ry = fcurves.new(data_path="rotation_quaternion", index=2)
	fcurve_rz = fcurves.new(data_path="rotation_quaternion", index=3)
	fcurve_px = fcurves.new(data_path="location", index=0)
	fcurve_py = fcurves.new(data_path="location", index=1)
	fcurve_pz = fcurves.new(data_path="location", index=2)

	def add_animation_data(f, odom):
		fcurve_rx.keyframe_points.insert(frame=f, value=odom["rot"]["x"])
		fcurve_ry.keyframe_points.insert(frame=f, value=odom["rot"]["y"])
		fcurve_rz.keyframe_points.insert(frame=f, value=odom["rot"]["z"])
		fcurve_rw.keyframe_points.insert(frame=f, value=odom["rot"]["w"])
		fcurve_px.keyframe_points.insert(frame=f, value=odom["pos"]["x"])
		fcurve_py.keyframe_points.insert(frame=f, value=odom["pos"]["y"])
		fcurve_pz.keyframe_points.insert(frame=f, value=odom["pos"]["z"])
	
	with open(config["odom_file"], "r") as odom_file:
		odom_json = json.loads(odom_file.read())
	
	anim_frame = 1
	for odom_data in odom_json["odom"]:
		add_animation_data(anim_frame, odom_data)
		anim_frame += 1

	anim_data = armature.animation_data_create()
	anim_data.action = action
	anim_data.action_slot = slot

add_anim_to_armature(armature_object)



#################
# CAMERA SCENES #
#################

'''
Because the cameras have different resolutions & framerates, they can't be rendered 
in a single pass using multiview. Each camera pass is rendered from its own scene, 
using the base_scene as linked source. Render settings, camera parameters, animation 
data and the source movie clip are adjusted for every camera.
'''

for camera_config in config["cameras"]:
	# Create scene
	bpy.ops.scene.new(type="LINK_COPY")
	scene = bpy.context.scene
	scene.name = camera_config["name"]

	# Create camera
	camera_data = bpy.data.cameras.new(camera_config["name"])
	camera_data.lens_unit = "FOV"
	camera_data.angle = 1.75

	camera_object = bpy.data.objects.new(camera_config["name"], camera_data)
	scene.collection.objects.link(camera_object)
	scene.camera = camera_object

	# Attach camera to animated bone
	camera_object.location = armature_object.location	# Move to bone to avoid rotation around diff-offset
	camera_object.rotation_euler = (-2.02, pi, 1.9)	# Rotation offset of recording
	constraint = camera_object.constraints.new("CHILD_OF")
	constraint.target = armature_object

	# Load source video
	movie_clip = bpy.data.movieclips.load(camera_config["image_path"])

	# Add video to compositing
	movie_node = scene.node_tree.nodes.get("Movie Clip")
	movie_node.clip = movie_clip

	# Add video to camera background (visible in GUI)
	if WITH_GUI:
		camera_data.show_background_images = True
		bg_image_collection = camera_data.background_images
		bg_image = bg_image_collection.new()
		bg_image.alpha = 1.0
		bg_image.source = "MOVIE_CLIP"
		bg_image.clip = movie_clip
	
	# Adjust render settings according to source video
	scene.frame_end = movie_clip.frame_duration

	resolution = movie_clip.size
	scene.render.resolution_x = resolution[0]
	scene.render.resolution_y = resolution[1]

	mkdir(f'{output_path}\\{camera_config["name"]}')
	digit_count = floor(log10(scene.frame_end) + 1)
	scene.render.filepath = f'//{camera_config["name"]}/{"#" * digit_count}'
	

# ChildOf constraint to fix to bone

# Place obstacle

# Define animation





##########
# RENDER #
##########

if not WITH_GUI:
	for camera_config in config["cameras"]:
		bpy.ops.render.render(animation=True, scene=camera_config["name"])

bpy.ops.wm.save_mainfile()