from core import load_config
from schema import generator_config_schema


def main():
	config = load_config(schema=generator_config_schema)
	print(config["cameras"])
	


if __name__ == "__main__":
	main()