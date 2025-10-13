from os.path import join
from json import dumps

from . import TopicExtractor

class DataTopicExtractor(TopicExtractor):
	def __init__(self, id, export_root):
		super().__init__(id, export_root)
		self.json_path = join(self.export_root, f"{self.id}.json")
		self.datapoints = []
		pass

	def before_extract(self):
		pass

	def after_extract(self):
		with open(self.json_path, "w") as json_file:
			json_file.write(dumps(self.datapoints))
