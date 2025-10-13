from . import ImageTopicExtractor

class CameraImageTopicExtractor(ImageTopicExtractor):
	def on_message(self, message, timestamp):
		if "jpeg" not in message.format:
			print(f"Unsupported image format: {message.format}")
			return

		self.timeinfo.append(timestamp)

		with open(self.get_image_path("jpg"), "wb") as image_file:
			image_file.write(message.data)
		
		self.current_index += 1
		