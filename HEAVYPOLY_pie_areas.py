bl_info = {
	"name": "Pie Areas",
	"description": "Area Types",
	"author": "Vaughan Ling",
	"version": (0, 1, 0),
	"blender": (2, 80, 0),
	"location": "",
	"warning": "",
	"wiki_url": "",
	"category": "Pie Menu"
	}

import bpy
from bpy.types import (
		Menu,
		Operator,
		)
import os

class HP_MT_pie_areas(Menu):
	bl_label = "Areas"

	def draw(self, context):
		layout = self.layout
		pie = layout.menu_pie() 	
		# left
#   	 pie.operator("wm.preview_render", text="Preview Render")

		split = pie.split()
		col = split.column(align=True)
		col.scale_y=1.5
		row = col.row(align=True)
		prop = col.operator("wm.context_set_enum", text="Timeline")
		prop.data_path = "area.type"
		prop.value = 'DOPESHEET_EDITOR'
		prop = col.operator("wm.context_set_enum", text="Graph Editor")
		prop.data_path = "area.type"
		prop.value = 'GRAPH_EDITOR'
		# right
		pie.operator("wm.3dview", text="3D View")
		# bottom
		#block
		split = pie.split()
		col = split.column(align=True)
		

		row = col.row(align=True)
		row.scale_y=1.5
		prop = row.operator("wm.context_set_enum", text="Text Editor")
		prop.data_path = "area.type"
		prop.value = 'TEXT_EDITOR'
		row = col.row(align=True)
		row.scale_y=1.5
		prop = row.operator("wm.context_set_enum", text="Python Console")
		prop.data_path = "area.type"
		prop.value = 'CONSOLE'  
		row = col.row(align=True)
		row.scale_y=1.5 	   
		row.operator('wm.hp_fullscreen', text='Fullscreen')
		# top
		pie.operator("screen.screen_full_area", text="Maximize")

		split = pie.split()
		col = split.column(align=True)
		row = col.row(align=True)
		row.scale_y=1.5
		prop = row.operator("wm.context_set_enum", text="IIMMG Editor")
		prop.data_path = "area.type"
		prop.value = 'IMAGE_EDITOR'
		prop = row.operator("wm.context_set_enum", text="UV Editor")
		prop.data_path = "area.type"
		prop.value = 'UV_EDITOR'

		prop = pie.operator("wm.context_set_enum", text="Shader Editor")
		prop.data_path = "area.type"
		prop.value = 'NODE_EDITOR'  	  
		prop = pie.operator("wm.context_set_enum", text="Outliner")
		prop.data_path = "area.type"
		prop.value = 'OUTLINER'  	 
		prop = pie.operator("wm.context_set_enum", text="Properties")
		prop.data_path = "area.type"
		prop.value = 'PROPERTIES'  	 
#		pie.operator("wm.areas_popup", text="Outliner Popup").area = 'OUTLINER'
		
		
class HP_OT_fullscreen(bpy.types.Operator):
	bl_idname = 'wm.hp_fullscreen'
	bl_label = ''
	def execute(self, context):
		bpy.ops.screen.screen_full_area()
		bpy.ops.wm.window_fullscreen_toggle()
		return {'FINISHED'}

class HP_OT_areas_preview_render(bpy.types.Operator):
	bl_idname = 'wm.preview_render'
	bl_label = 'Preview Render'
	def execute(self, context):
		bpy.ops.wm.context_set_enum(data_path='area.type', value='VIEW_3D')
		bpy.ops.view3d.view_camera()
		bpy.context.space_data.overlay.show_overlays = False
		return {'FINISHED'}

class HP_OT_areas_3d_view(bpy.types.Operator):
	bl_idname = 'wm.3dview'
	bl_label = '3D View, material'
	def execute(self, context):
		bpy.ops.wm.context_set_enum(data_path='area.type', value='VIEW_3D')
		return {'FINISHED'}

class HP_OT_areas_popup(bpy.types.Operator):
	bl_idname = 'wm.areas_popup'
	bl_label = ''
	area: bpy.props.StringProperty(name="Area")	
	def execute(self, context):
		ui = bpy.context.area.ui_type
		bpy.context.area.ui_type =  self.area
		bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
		bpy.context.area.ui_type =  ui
		return {'FINISHED'}

class HP_OT_texture_paint_toggle(bpy.types.Operator):
	bl_idname = 'wm.texture_paint_toggle'
	bl_label = 'Texture Paint Toggle'
	def execute(self, context):
		bpy.ops.object.mode_set(mode='TEXTURE_PAINT', toggle=False)  
		return {'FINISHED'}

classes = (
	HP_MT_pie_areas,
	HP_OT_areas_preview_render,
	HP_OT_areas_3d_view,
	HP_OT_areas_popup,
	HP_OT_texture_paint_toggle,
	HP_OT_fullscreen
)
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
	register()