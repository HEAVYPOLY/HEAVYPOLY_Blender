
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

	def modal(self, context, event):
		bpy.context.space_data.shading.show_xray = True
		if event.type == 'MOUSEMOVE' and event.value == 'PRESS':
			bpy.ops.view3d.select_box('INVOKE_DEFAULT',mode='SET',wait_for_input=False)
			return {'RUNNING_MODAL'}
		if event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
			bpy.context.space_data.shading.show_xray = False
			return {'CANCELLED'}
		elif event.type == 'MOUSEMOVE' and event.value == 'RELEASE':
			bpy.context.space_data.shading.show_xray = False
			return {'CANCELLED'}
		return {'RUNNING_MODAL'}
	def invoke(self, context, event):
		if bpy.context.space_data.shading.show_xray == True:
			bpy.ops.view3d.select_box('INVOKE_DEFAULT',mode='SET',wait_for_input=False)
		else:
			context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}
   # [("view3d.select_box",
     # {"type": 'EVT_TWEAK_L', "value": 'ANY'},
     # {"properties":
      # [("wait_for_input", True),
       # ],
class HP_OT_select_through_border_add(bpy.types.Operator):
	bl_idname = "view3d.select_through_border_add"
	bl_label = "Select Through Border"

	def modal(self, context, event):
		
		bpy.context.space_data.shading.show_xray = True
		if event.type == 'MOUSEMOVE' and event.value == 'PRESS':
			bpy.ops.view3d.select_box('INVOKE_DEFAULT',mode='ADD',wait_for_input=False)
			return {'RUNNING_MODAL'}
		if event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
			bpy.context.space_data.shading.show_xray = False
			return {'CANCELLED'}
		elif event.type == 'MOUSEMOVE' and event.value == 'RELEASE':
			bpy.context.space_data.shading.show_xray = False
			return {'CANCELLED'}
		return {'RUNNING_MODAL'}
	def invoke(self, context, event):
		if bpy.context.space_data.shading.show_xray == True:
			bpy.ops.view3d.select_box('INVOKE_DEFAULT',mode='ADD',wait_for_input=False)
		else:
			context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

class HP_OT_select_through_border_sub(bpy.types.Operator):
	bl_idname = "view3d.select_through_border_sub"
	bl_label = "Select Through Border"

	def modal(self, context, event):
		bpy.context.space_data.shading.show_xray = True
		if event.type == 'MOUSEMOVE' and event.value == 'PRESS':
			bpy.ops.view3d.select_box('INVOKE_DEFAULT',mode='SUB',wait_for_input=False)
			return {'RUNNING_MODAL'}
		if event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
			bpy.context.space_data.shading.show_xray = False
			return {'CANCELLED'}
		elif event.type == 'MOUSEMOVE' and event.value == 'RELEASE':
			bpy.context.space_data.shading.show_xray = False
			return {'CANCELLED'}
		return {'RUNNING_MODAL'}
	def invoke(self, context, event):
		if bpy.context.space_data.shading.show_xray == True:
			bpy.ops.view3d.select_box('INVOKE_DEFAULT',mode='SUB',wait_for_input=False)
		else:
			context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

classes = (
	HP_OT_select_through_border,
	HP_OT_select_through_border_add,
	HP_OT_select_through_border_sub,
)
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
	register()