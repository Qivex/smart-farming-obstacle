from os import mkdir
from os.path import join
from json import dumps

from . import TopicExtractor
from core.const import TIMEINFO_FILENAME, IMAGE_FILE_FORMATSTRING



class ImageTopicExtractor(TopicExtractor):
	def __init__(self, id, export_root):
		super().__init__(id, export_root)
		self.image_path = join(self.export_root, self.id)
		self.timeinfo_path = join(self.image_path, TIMEINFO_FILENAME)
		self.timeinfo = []
		self.current_index = 1
		pass


	def before_extract(self):
		# Create folder to contain exported images
		mkdir(self.image_path)


	def after_extract(self):
		# Write timestamp of each image into json. Required for correct timing of animation data
		with open(self.timeinfo_path, "w") as timeinfo_file:
			timeinfo_file.write(dumps(self.timeinfo))


	def get_image_path(self, format):
		image_filename = IMAGE_FILE_FORMATSTRING.format(id=self.id, index=self.current_index, format=format)
		return join(self.image_path, image_filename)


	def append_timestamp(self, stamp):
		timestamp = stamp.sec * 10e9 + stamp.nsec
		self.timeinfo.append(timestamp)
