from os.path import join

from numpy import interp

from common import load_json
from .ValueCalculator import ValueCalculator


# Resolve JSON path (= array) in data
def value_from_json_path(data, jsonpath):
	target_value = data
	for key in jsonpath:
		if key not in target_value:
			return None
		target_value = target_value[key]
	return target_value


class DataHandler:
	def __init__(self, import_mapping):
		self.import_mapping = import_mapping

	def load_data(self, path):
		data = {}
		for entry in self.import_mapping:
			filename = entry["file"]
			# Load data
			file_data = load_json(join(path, filename), "animation data")
			if "calculatedValues" in entry:
				# Calculate additional values from expressions
				ValueCalculator(entry["calculatedValues"]).execute_calculations(file_data)
				# Add these to mapping
				for calculated_value in entry["calculatedValues"]:
					entry["values"].append({
						"jsonPath": ["calculated", calculated_value["key"]],
						"assignedKey": calculated_value["key"]
					})
			data[filename] = file_data
		self.source_data = data
	
	def interpolate_values(self, required_timestamps):
		result = {}
		for required_source in self.import_mapping:
			source_name = required_source["file"]
			if source_name not in self.source_data:
				print(f"Data from file {required_source['file']} was not loaded!")
				break
			data = self.source_data[source_name]
			# Collect all XY-pairs (timestamp, value) for interpolation
			provided_timestamps = [datapoint["time"] for datapoint in data]
			for required_value in required_source["values"]:
				provided_values = [value_from_json_path(datapoint, required_value["jsonPath"]) for datapoint in data]
				# Interpolate values
				result[required_value["assignedKey"]] = interp(required_timestamps, provided_timestamps, provided_values)
		return result