from . import SceneSetup
from generator.compositing import DepthSceneCompositor


class DepthSceneSetup(SceneSetup):
	def setup(self, config):
		DepthSceneCompositor(self.scene, config["export"]["generateAlphaMaps"])