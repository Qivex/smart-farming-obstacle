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

from common import load_config
from common.const import PANORAMA_SENSOR_PARTITION_AMOUNT
from schema import generator_config_schema

from generator.setup import BaseSceneSetup, CameraSceneSetup, DepthSceneSetup, SensorSceneSetup

from generator.animation import DataInterpolator, KeyframeGenerator


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
	interpolator = DataInterpolator(config["animation"]["sourceMapping"])
	interpolator.load_data(config["dataPath"])
	keyframe_generator = KeyframeGenerator(interpolator, config["animation"]["boneMapping"])

	# Create a scene for each sensor or part:
	render_scenes = []
	for sensor in config["sensors"]:
		if sensor["type"] == "camera":
			scene = SensorSceneSetup().create_scene(camera_base_scene, sensor["id"], {
				"sensor": sensor,
				"root": config["dataPath"],
				"keyframes": keyframe_generator
			})
			render_scenes.append(scene)
		elif sensor["type"] == "lidar":
			# for part in range(PANORAMA_SENSOR_PARTITION_AMOUNT):
			part = 1
			scene = SensorSceneSetup().create_scene(depth_base_scene, f"{sensor['id']}_part{part}", {
				"sensor": sensor,
				"part": part,	# Only required for scenes with parts!
				"root": config["dataPath"],
				"keyframes": keyframe_generator,
			})
			render_scenes.append(scene)
		
	# TODO
	for scene in render_scenes:
		print(f"Rendering {scene.name}")
		# bpy.ops.render.render(scene=scene.name, animation=True)

	# Before closing
	bpy.ops.object.select_all(action="DESELECT")
	bpy.ops.wm.save_mainfile()


if __name__ == "__main__":
	main()