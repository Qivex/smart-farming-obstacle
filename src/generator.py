#################
# BLENDER SETUP #
#################

from math import floor
from os import makedirs
from os.path import dirname, realpath, join
from sys import exit, path
from time import time

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

from common import load_config, load_json
from schema import generator_config_schema

from generator.animation.keyframes import create_animation2
from generator.setup import BaseSceneSetup, CameraSceneSetup, DepthSceneSetup, SensorSceneSetup

from generator.animation import DataHandler, KeyframeGenerator
from common import load_json


def main():
	config = load_config(schema=generator_config_schema)
	# Todo: Check config content for additional details not verifiable with schema (e.g. boneID's actually match)
	
	# Copy Blender project to new file
	try:
		selected_directory = f'{realpath(config["output"]["exportPath"])}@{floor(time())}'
		makedirs(selected_directory)
	except Exception as e:
		print(f"Error while creating output directory:\n\t{e}")

	try:
		bpy.ops.wm.save_as_mainfile(filepath=join(selected_directory, "project.blend"))
	except Exception as e:
		print(f"Error while creating project copy:\n\t{e}")
	
	# Shared scene setup & armature
	base_scene = BaseSceneSetup().create_scene(bpy.context.scene, "base_scene", config)

	# Shared compositing logic
	camera_base_scene = CameraSceneSetup().create_scene(base_scene, "camera_base_scene", config)
	depth_base_scene = DepthSceneSetup().create_scene(base_scene, "depth_base_scene", config)
	

	# Shared animation data
	data_handler = DataHandler(config["animation"]["sourceMapping"])
	data_handler.load_data(config["dataPath"])
	keyframe_generator = KeyframeGenerator(data_handler, config["animation"]["boneMapping"])

	# Example Scenes
	cam_config = {
		"root": config["dataPath"],
		"img": "zed_left/zed_left-1.jpg",
		"id": "zed_left",
		"kg": keyframe_generator
	}

	lidar_config = {
		"root": config["dataPath"],
		"img": "ouster/ouster_part1-1.exr",
		"id": "ouster",
		"kg": keyframe_generator
	}

	example_camera_scene = SensorSceneSetup().create_scene(camera_base_scene, "example_sensor_scene", cam_config)
	example_lidar_scene = SensorSceneSetup().create_scene(depth_base_scene, "example_lidar_scene", lidar_config)


	# TEST
	return
	am = AnimationManager("linear")
	am.load_data_from_sources("d:/Uni/Bachelorarbeit/Smart Farming Lab/Code/smart-farming-obstacle/test/export-full@1763028961", ["gps.json", "zed_odom.json"])
	am.set_mapping_config(config["animation"]["sourceMapping"])

	required_timestamps = load_json("d:/Uni/Bachelorarbeit/Smart Farming Lab/Code/smart-farming-obstacle/test/export-full@1763028961/zed_left/timeinfo.json", "timestamps")
	
	values = am.interpolate_values(required_timestamps)

	for entry in values.values():
		print(len(entry))

	return
	# Seperate image source, animation & rendering for each sensor
	for sensor in config["sensors"]:
		pass

	# Render

	
	return
	# Test animation
	zed_odom_data = load_json("d:/Uni/Bachelorarbeit/Smart Farming Lab/Code/smart-farming-obstacle/test/export-zed@1762934416/zed_odom.json", "odom")
	create_animation2(armature, config["animationMapping"], zed_odom_data)


	return
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