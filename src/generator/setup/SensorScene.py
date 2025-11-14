from . import Scene

def SensorScene(Scene):
	def add_animation(self):
		pass

	def set_movie_clip(self, movie_clip):
		# Adjust viewport size
		render_settings = self.scene.render
		render_settings.resolution_x, render_settings.resolution_y = movie_clip.size
		# Set source of movie node in compositor
		movie_node = self.scene.node_tree.nodes.get("Movie Clip")
		movie_node.clip = movie_clip