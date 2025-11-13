import bpy

# TODO: Use bpy.context.collection.all_objects to get objects of current scene only

class Scene:
	def __init__(self, name, scene):
		# Activate parent scene (because operator always applies to active scene)
		bpy.context.window.scene = scene
		# Create new scene by copying from an existing scene
		bpy.ops.scene.new(type="FULL_COPY")
		self.scene = bpy.context.scene
		self.scene.name = name
	
	def activate(self):
		bpy.context.window.scene = self.scene