from . import ImageTopicExtractor



class CameraImageTopicExtractor(ImageTopicExtractor):
	def __init__(self, id, export_root):
		super().__init__(id, export_root)
	

	def on_message(self, message):
		if "jpeg" not in message.format:
			print(f"Unsupported image format: {message.format}")
			return

		self.append_timestamp(message.stamp)

		with open(self.get_image_path("jpg")) as image_file:
			image_file.write(message.data)
		self.current_index += 1
		