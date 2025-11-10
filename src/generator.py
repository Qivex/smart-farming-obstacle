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


def main():
	config = load_config(schema=generator_config_schema)
	# Todo: Check config content for additional details not verifiable with schema
	create_armature(config["bones"])


if __name__ == "__main__":
	main()