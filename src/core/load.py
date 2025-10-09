from argparse import ArgumentParser
from json import loads
from json.decoder import JSONDecodeError
from jsonschema import validate, ValidationError, SchemaError
from sys import exit


def __validate_config(config, schema):
	try:
		validate(config, schema)
	except SchemaError as e:
		print(f"Schema used for validation is not valid:\n\t{e.message}")
		exit()
	except ValidationError as e:
		print(f"Provided config is not valid:\n\t{e.message}")
		exit()


def load_config(schema=None):
	parser = ArgumentParser()
	parser.add_argument("--config", "-c", required=True, metavar="path", help="path to config file")
	arguments = parser.parse_args()
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