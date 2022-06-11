
bl_info = {
	"name": "Border Select Through",
	"description": "Border Select through a mesh",
	"author": ("Vaughan Ling"),
	"version": (0, 1, 0),
	"blender": (2, 80, 0),
	"location": "",
	"warning": "",
	"wiki_url": "",
	"category": "Pie Menu"
	}

import bpy
import bgl
from mathutils import Vector
from bpy.props import IntProperty, BoolProperty

class HP_OT_select_through_border(bpy.types.Operator):
	bl_idname = "view3d.select_through_border"
	bl_label = "Select Through Border"
	def execute(self, context):
		print("EXECUTE")

	def modal(self, context, event):
		if event.type == "MOUSEMOVE":
			bpy.context.space_data.shading.show_xray = False
			return {'CANCELLED'}

		elif event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
			bpy.context.space_data.shading.show_xray = False
			print("LEFTMOUSE RELEASE")
			return {'CANCELLED'}
		elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
			bpy.context.space_data.shading.show_xray = False
			print("CANCELLED")
			return {'CANCELLED'}
		return {'RUNNING_MODAL'}
	def invoke(self, context, event):
		bpy.context.space_data.shading.show_xray = True
		print("INVOKE !")
		context.window_manager.modal_handler_add(self)
		bpy.ops.view3d.select_box('INVOKE_DEFAULT',mode='SET',wait_for_input=False)
		return {'RUNNING_MODAL'}

class HP_OT_select_through_border_add(bpy.types.Operator):
	bl_idname = "view3d.select_through_border_add"
	bl_label = "Select Through Border"

	def modal(self, context, event):
		if event.type == "MOUSEMOVE":
			bpy.context.space_data.shading.show_xray = False
			return {'CANCELLED'}

		elif event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
			bpy.context.space_data.shading.show_xray = False
			print("LEFTMOUSE RELEASE")
			return {'CANCELLED'}
		elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
			bpy.context.space_data.shading.show_xray = False
			print("CANCELLED")
			return {'CANCELLED'}
		return {'RUNNING_MODAL'}
	def invoke(self, context, event):
		bpy.context.space_data.shading.show_xray = True
		print("INVOKE !")
		context.window_manager.modal_handler_add(self)
		bpy.ops.view3d.select_box('INVOKE_DEFAULT',mode='ADD',wait_for_input=False)
		return {'RUNNING_MODAL'}

class HP_OT_select_through_border_sub(bpy.types.Operator):
	bl_idname = "view3d.select_through_border_sub"
	bl_label = "Select Through Border"

	def modal(self, context, event):
		if event.type == "MOUSEMOVE":
			bpy.context.space_data.shading.show_xray = False
			return {'CANCELLED'}

		elif event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
			bpy.context.space_data.shading.show_xray = False
			print("LEFTMOUSE RELEASE")
			return {'CANCELLED'}
		elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
			bpy.context.space_data.shading.show_xray = False
			print("CANCELLED")
			return {'CANCELLED'}
		return {'RUNNING_MODAL'}
	def invoke(self, context, event):
		bpy.context.space_data.shading.show_xray = True
		print("INVOKE !")
		context.window_manager.modal_handler_add(self)
		bpy.ops.view3d.select_box('INVOKE_DEFAULT',mode='SUB',wait_for_input=False)
		return {'RUNNING_MODAL'}

classes = (
	HP_OT_select_through_border,
	HP_OT_select_through_border_add,
	HP_OT_select_through_border_sub,
)
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
	register()
