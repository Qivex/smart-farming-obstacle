from abc import ABC, abstractmethod

class Topic(ABC):
	def __init__(self, id, export_root):
		self.id = id
		self.export_root = export_root

	@abstractmethod
	def before_extract(self):
		pass

	@abstractmethod
	def on_message(self, message):
		pass

	@abstractmethod
	def after_extract(self):
		pass