from . import DataTopicExtractor

class GPSDataTopicExtractor(DataTopicExtractor):
	def on_message(self, message, timestamp):
		self.datapoints.append({
			"time": timestamp,
			"lat": message.lat,
			"lon": message.lon,
			"hgt": message.hgt
		})