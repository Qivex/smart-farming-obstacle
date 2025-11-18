from numpy import interp

from common import load_json


# Resolve JSON path (= array) in data
def value_from_json_path(data, jsonpath):
	target_value = data
	for key in jsonpath:
		if key not in target_value:
			return None
		target_value = target_value[key]
	return target_value


class AnimationManager:
	def __init__(self, interpolation_mode):
		self.interpolation_mode = interpolation_mode
		pass

	def load_data_from_sources(self, path, files):
		self.source_data = {filename: load_json(f"{path}/{filename}", "animation data") for filename in files}

	def set_mapping_config(self, config):
		self.key_mapping = config
	
	def interpolate_values(self, required_timestamps):
		result = {}

		for required_source in self.key_mapping:
			source_name = required_source["file"]
			if source_name not in self.source_data:
				print(f"Data from file {required_source['file']} was not loaded!")
				break
			data = self.source_data[source_name]
			# Collect all XY-pairs (timestamp, value) for interpolation
			provided_timestamps = [datapoint["time"] for datapoint in data]
			print(f"{source_name} = {len(provided_timestamps)}")
			for required_value in required_source["values"]:
				provided_values = [value_from_json_path(datapoint, required_value["jsonPath"]) for datapoint in data]
				# Interpolate values
				result[required_value["assignedKey"]] = interp(required_timestamps, provided_timestamps, provided_values)
		
		return result