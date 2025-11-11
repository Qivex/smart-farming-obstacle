#################
# BLENDER SETUP #
#################

from sys import exit, path
from os.path import dirname, realpath, join

# Check if script run using Blender:
try:
	import bpy
except ImportError:
	print("This script must be run using Blender! Available options:")
	print("- Open Blender GUI and load this file as a script:\n\tWorkspace 'Scripting' -> Open")
	print("- Execute this script from console:\n\tblender --background --python [this-script] -- --config [your-config]")
	exit()

# Provide module path to enable relative imports:
# - Blender uses its own Python environment
# - See https://blender.stackexchange.com/a/33622
module_directory = dirname(realpath(__file__))
path.append(module_directory)
path.append(join(module_directory, "Lib", "site-packages"))



#############
# GENERATOR #
#############

from core import load_config
from schema import generator_config_schema

from generator.armature import create_armature
from generator.compositing import LidarSceneCompositor


def main():
	config = load_config(schema=generator_config_schema)
	# Todo: Check config content for additional details not verifiable with schema
	
	# Test armature creation
	# create_armature(config["bones"])

	# Test lidar compositing
	scene = bpy.context.scene
	scene.eevee.taa_render_samples = 1
	scene.render.resolution_x = 171
	scene.render.resolution_y = 128
	for i in range(3):
		bpy.ops.scene.new(type="FULL_COPY")
		scene = bpy.context.scene
		scene.name = f"lidar_part{i}"
		# Different Camera FOVs to distinct scenes
		camera_data = scene.camera.data
		print(camera_data)
		camera_data.lens_unit = "FOV"
		camera_data.angle = 1 + 0.25*i
	bpy.ops.scene.new(type="EMPTY")
	panorama_scene = bpy.context.scene
	panorama_scene.name = "lidar"
	panorama_scene.render.resolution_x = 512
	test_compositor = LidarSceneCompositor(panorama_scene)
	# test_compositor.set_movie_clip(None)


if __name__ == "__main__":
	main()