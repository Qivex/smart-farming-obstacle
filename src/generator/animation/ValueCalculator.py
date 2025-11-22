import math

class ValueCalculator:
	def __init__(self, expression_config):
		evals = {}
		for entry in expression_config:
			key = entry["key"]
			expression = entry["expression"]
			try:
				evals[key] = eval(expression, {"math": math})
			except Exception as e:
				print(f'Failed to parse expression for calculated value "{key}":\n\t{e}')
		self.user_functions = evals
	
	def execute_calculations(self, data):
		for index, value in enumerate(data):
			value["calculated"] = {}
			for key, func in self.user_functions.items():
				try:
					value["calculated"][key] = func(data, index)
				except Exception as e:
					print(f'Error when calculating value "{key}" for index {index}:\n\t{e}')
