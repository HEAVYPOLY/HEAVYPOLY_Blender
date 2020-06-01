bl_info = {
	"name": "Pie View",
	"description": "View Modes",
	"author": "Vaughan Ling",
	"version": (0, 1, 0),
	"blender": (2, 80, 0),
	"location": "",
	"warning": "",
	"wiki_url": "",
	"category": "Pie Menu"
	}


import bpy
from bpy.types import Menu

# View Pie with left meaning left of model vs Blender defaults

class HP_MT_pie_view(Menu):
	bl_label = "View"

	def draw(self, context):
		layout = self.layout

		pie = layout.menu_pie()
		# left
		pie.operator("view3d.view_axis", text="Left").type = "LEFT"
		# right
		pie.operator("view3d.view_axis", text="Right").type = "RIGHT"
		# bottom
		split = pie.split()
		col = split.column(align=True)
		col.scale_y=1.5
		col.operator("view3d.view_camera", text="View Cam")
		row = col.row(align=True)
		row.alignment = 'CENTER'
		row.operator("view3d.create_camera_at_view", text="New Cam")
		prop = row.operator("wm.context_toggle", text="Lock Cam")
		prop.data_path = "space_data.lock_camera"
		col.scale_y=1.5
		row = col.row(align=True)
		row.alignment = 'EXPAND'
		row.operator("view3d.navigate", text="Walk")
		prop = row.operator("view3d.view_axis", text="Align")
		prop.align_active = True
		prop.type = 'TOP'
		scene = context.scene
		rd = scene.render
		prop = scene.eevee
		image_settings = rd.image_settings
		col.separator
		col.scale_x=1.3
		col.label(text='ACTIVE CAMERA')
		col.prop(scene, "camera", text = '')
		col.separator
		col.scale_x=1.3
		# col.operator("view3d.render_presets", text="Render Viewport To Movie").type = 'Viewport To Movie'
		# col.operator("view3d.render_presets", text="Low Render Animation").type = 'Low Render Animation'
		# col.operator("view3d.render_presets", text="Mid Render Animation").type = 'Mid Render Animation'
		# col.operator("view3d.render_presets", text="High Render Animation").type = 'High Render Animation'
		# col.operator("view3d.render_presets", text="Final Render Animation").type = 'Final Render Animation'


		# top
		pie.operator("view3d.view_axis", text="Top").type = "TOP"
		# topleft
		pie.operator("view3d.view_axis", text="Back").type = "BACK"
		# topright
		pie.operator("view3d.view_axis", text="Front").type = "FRONT"
		# bottomleft

		# bottomright
		pie.operator("view3d.view_axis", text="Bottom").type = "BOTTOM"

		pie.operator("view3d.view_persportho", text="Perspective / Ortho")
		# pie.operator("view3d.view_selected", text="Zoom to Selected")



class HP_OT_render_presets(bpy.types.Operator):
	bl_idname = "view3d.render_presets"
	bl_label = "HP Render Presets"
	bl_options = {'REGISTER', 'UNDO'}
	type: bpy.props.StringProperty(name="Type")

	def execute(self, context):
		scene = bpy.context.scene
		##VIEWPORT RENDER
		scene.render.use_border = True
		if bpy.context.area.spaces.active.region_3d.view_perspective == 'CAMERA':
			print('Already In Camera View')
		else:
			bpy.ops.view3d.view_camera()

		if self.type == 'Viewport To Movie':
			scene.render.resolution_percentage = 100
			bpy.context.space_data.overlay.show_overlays = False
			scene.render.image_settings.file_format = 'FFMPEG'
			# print('quicktime')
			# print(bpy.context.scene.render.ffmpeg.format)
			bpy.context.scene.render.ffmpeg.format = 'QUICKTIME'

		if self.type == 'Low Render Animation':
		##FINAL RENDER##
			bpy.context.scene.render.engine = 'CYCLES'
			scene.render.resolution_percentage = 25
			scene.frame_step = 2
			scene.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
			scene.render.image_settings.color_mode = 'RGBA'
			bpy.context.scene.cycles.samples = 256
			# bpy.ops.render.render(animation=True)
		if self.type == 'Mid Render Animation':
		##FINAL RENDER##
			bpy.context.scene.render.engine = 'CYCLES'
			scene.render.resolution_percentage = 50
			scene.frame_step = 2
			scene.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
			scene.render.image_settings.color_mode = 'RGBA'
			bpy.context.scene.cycles.samples = 512
			# bpy.ops.render.render(animation=True)
		if self.type == 'High Render Animation':
		##FINAL RENDER##
			bpy.context.scene.render.engine = 'CYCLES'
			scene.render.resolution_percentage = 100
			scene.frame_step = 1
			scene.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
			scene.render.image_settings.color_mode = 'RGBA'
			bpy.context.scene.cycles.samples = 1024
			# bpy.ops.render.render(animation=True)
		if self.type == 'Final Render Animation':
		##FINAL RENDER##
			bpy.context.scene.render.engine = 'CYCLES'
			scene.render.resolution_percentage = 100
			scene.frame_step = 1
			scene.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
			scene.render.image_settings.color_mode = 'RGBA'
			bpy.context.scene.cycles.samples = 2048
			# bpy.ops.render.render(animation=True)
		return {'FINISHED'}


class HP_OT_create_camera_at_view(bpy.types.Operator):
	bl_idname = "view3d.create_camera_at_view"
	bl_label = "Create Camera At View"
	bl_options = {'REGISTER', 'UNDO'}

	def invoke(self, context, event):
		def create_camera_at_view():
			bpy.ops.object.camera_add()
			bpy.context.object.data.passepartout_alpha = 1
			bpy.context.object.data.dof.aperture_fstop = 5
			bpy.context.object.data.dof.aperture_blades = 6
			bpy.context.object.data.dof.focus_distance = 2
			bpy.context.object.data.lens = 50
			bpy.context.object.data.show_name = True
			bpy.context.object.show_name = True
			active_cam = bpy.context.active_object
			bpy.context.scene.camera = active_cam
			bpy.ops.view3d.camera_to_view()
			bpy.context.space_data.lock_camera = True

			try:
				bpy.data.collections['Cameras']
			except:
				print('Creating Cameras Collection')
				col = bpy.data.collections.new("Cameras")
				bpy.context.scene.collection.children.link(col)
			try:
				bpy.context.scene.collection.objects.unlink(active_cam)
			except:
				for c in bpy.data.collections:
					try:
						c.objects.unlink(active_cam)
					except:
						pass
			bpy.data.collections['Cameras'].objects.link(active_cam)
			active_cam.select_set(state=True)
			bpy.context.view_layer.objects.active = active_cam
		if bpy.context.area.spaces.active.region_3d.view_perspective == 'CAMERA':
			print('Switching to Right View')
			bpy.ops.view3d.view_axis(type='RIGHT')
		try:
			bpy.ops.object.mode_set(mode='OBJECT', toggle = False)
		except:
			pass
		create_camera_at_view()
		return {'FINISHED'}

def register():
	bpy.utils.register_class(HP_MT_pie_view)
	bpy.utils.register_class(HP_OT_create_camera_at_view)
	bpy.utils.register_class(HP_OT_render_presets)

def unregister():
	bpy.utils.unregister_class(HP_MT_pie_view)
	bpy.utils.unregister_class(HP_OT_create_camera_at_view)
	bpy.utils.unregister_class(HP_OT_render_presets)

if __name__ == "__main__":
	register()
