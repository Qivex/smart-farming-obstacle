from . import DataTopicExtractor

class OdometryDataTopicExtractor(DataTopicExtractor):
	def on_message(self, message, timestamp):
		pose = message.pose.pose
		pos = pose.position
		rot = pose.orientation
		self.datapoints.append({
			"time": timestamp,
			"pos": {
				"x": pos.x,
				"y": pos.y,
				"z": pos.z
			},
			"rot": {
				"x": rot.x,
				"y": rot.y,
				"z": rot.z,
				"w": rot.w
			}
		})