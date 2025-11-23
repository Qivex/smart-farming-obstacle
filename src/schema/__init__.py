from os.path import realpath, dirname, join

from common import load_json

__dir = dirname(realpath(__file__))

extractor_config_schema = load_json(join(__dir, "extractor.config.schema.json"), "schema")
generator_config_schema = load_json(join(__dir, "generator.config.schema.json"), "schema")
validator_config_schema = load_json(join(__dir, "validator.config.schema.json"), "schema")