from argparse import ArgumentParser
from json import loads
from json.decoder import JSONDecodeError
from jsonschema import validate, ValidationError, SchemaError
from sys import exit, argv


def __validate_config(config, schema):
	try:
		validate(config, schema)
	except SchemaError as e:
		print(f"Schema used for validation is not valid:\n\t{e.message}")
		exit()
	except ValidationError as e:
		print(f"Provided config is not valid:\n\t{e.message}")
		exit()


def __parse_args(parser):
	try:
		# Blender ignores arguments AFTER "--" (See https://blender.stackexchange.com/a/8405)
		double_dash_index = argv.index("--") + 1
		# argpase should ignore Blender specific arguments BEFORE "--"
		return parser.parse_args(argv[double_dash_index:])
	except ValueError:
		# Default parsing when executed using python interpreter
		return parser.parse_args()


def load_config(schema=None):
	parser = ArgumentParser()
	parser.add_argument("--config", "-c", required=True, metavar="path", help="path to config file")
	arguments = __parse_args(parser)
	config = load_json(arguments.config, "config")
	if schema != None:
		__validate_config(config, schema)
	return config


def load_json(path, name):
	try:
		with open(path) as file:
			return loads(file.read())
	except FileNotFoundError as e:
		print(f"No {name} file found at provided path:\n\t{e.filename}")
		exit()
	except JSONDecodeError as e:
		print(f"Invalid JSON in {name} file:\n\t{e}")
		exit()