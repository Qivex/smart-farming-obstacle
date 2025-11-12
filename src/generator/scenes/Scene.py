import bpy

# TODO: Use bpy.context.collection.all_objects to get objects of current scene only

class Scene:
	def __init__(self, name):
		bpy.ops.scene.new(type="FULL_COPY")
		self.scene = bpy.context.scene
		self.scene.name = name
	
	def activate(self):
		bpy.context.window.scene = self.scene