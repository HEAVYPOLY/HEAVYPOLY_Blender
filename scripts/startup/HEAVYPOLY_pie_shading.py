bl_info = {
    "name": "Pie Shading",
    "description": "Shading Modes",
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

class HP_MT_pie_shading(Menu):
    bl_label = "Shading"
    bl_space_type = 'VIEW_3D'
    def draw(self, context):

        layout = self.layout

        view = context.space_data
        shading = view.shading
        obj = context.active_object
        overlay = view.overlay
        tool_settings = context.tool_settings
        object_mode = 'OBJECT' if obj is None else obj.mode
        pie = layout.menu_pie()
        #LEFT
        pie.prop_enum(view.shading, "type", value='WIREFRAME', icon = 'NONE', text = 'WIRE')
        #RIGHT
        
        split = pie.split()
        #BOTTOM
        # split = pie.split()
        # col = split.column(align=True)
        # row = col.row(align=True)
        # row.scale_y=1.5
        # row.operator('popup.hp_properties', text='World Settings').type='WORLD'
        # row = col.row(align=True)
        # row.scale_y=1.5
        # row.operator('popup.hp_render', text='Render Settings')
        # row = col.row(align=True)
        # row.scale_y=1.5
        # row.operator('render.render', text='Render Animation').animation=True
        # row = col.row(align=True)
        # row.scale_y=1.5
        # row.operator('render.render', text='Render Image')
        view = context.space_data
        
        pie.operator('view3d.localview', text='ISOLATE').frame_selected = False
        #TOP
        pie.prop_enum(view.shading, "type", value='MATERIAL', icon = 'NONE', text = 'MATERIAL')

        #TOP LEFT
        pie.prop_enum(view.shading, "type", value='SOLID', icon = 'NONE', text = 'SOLID')

        #TOP RIGHT
        pie.prop_enum(view.shading, "type", value='RENDERED', icon = 'NONE', text = 'RENDERED')

        #BOTTOM LEFT
        split = pie.split()
        col = split.column(align=True)
#        row = col.row(align=True)
#        row.scale_y=1.5
#        row.operator("shading.bg_wire", text='BG Wire')
        row = col.row(align=True)
        row.scale_y=1.5
        row.operator("scene.light_cache_bake", text='Bake Lighting')
        row = col.row(align=True)
        row.scale_y=1.5
        row.operator("scene.light_cache_free", text='Free Lighting')

        #BOTTOM RIGHT
        split = pie.split()
        col = split.column(align=True)
        col.scale_y=1.4

        box = col.box()
        box.prop(overlay, "show_overlays", text="OVERLAYS")
        box.prop(overlay, "show_extras", text="EXTRAS")
        box.prop(context.scene.eevee, "use_soft_shadows", text="SOFT SHADOWS")
        # box.prop(overlay, "show_backface_culling", text="HIDE BACKFACES")
        box.prop(overlay, "show_cursor", text="3D CURSOR")
        box.operator("view3d.smart_shade_smooth_toggle", text = 'Shade Smooth')
#        pie.operator("view3d.toggle_background_hide", text="Toggle BG Hide")


class HP_OT_shading_wire(bpy.types.Operator):
    bl_idname = "shading.wire"
    bl_label = "hp_shading_wire"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        bpy.data.screens["Default"].shading.type = 'SOLID'

        bpy.ops.view3d.toggle_shading(type='WIREFRAME')
        bpy.context.space_data.shading.show_xray = True
        bpy.context.space_data.shading.xray_alpha = 1
        bpy.context.space_data.shading.show_object_outline = 1
        
        return {'FINISHED'}
    
class HP_OT_shading_material(bpy.types.Operator):
    bl_idname = "shading.material"
    bl_label = "hp_shading_material"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        bpy.ops.view3d.toggle_shading(type='MATERIAL')
        bpy.context.space_data.shading.show_xray = False
        bpy.context.space_data.shading.xray_alpha = 0
        return {'FINISHED'}
    
class HP_OT_shading_solid(bpy.types.Operator):
    bl_idname = "shading.solid"
    bl_label = "hp_shading_wire"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        bpy.ops.view3d.toggle_shading(type='SOLID')
        bpy.context.space_data.shading.show_xray = False
        bpy.context.space_data.shading.xray_alpha = 0
        return {'FINISHED'}
        
class HP_OT_shading_rendered(bpy.types.Operator):
    bl_idname = "shading.rendered"
    bl_label = "hp_shading_rendered"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        bpy.ops.view3d.toggle_shading(type='RENDERED')
        bpy.context.space_data.shading.show_xray = False
        bpy.context.space_data.shading.xray_alpha = 0
        return {'FINISHED'}
        
class HP_OT_shading_bg_wire(bpy.types.Operator):
    bl_idname = "shading.bg_wire"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        for ob in bpy.context.selected_objects:
            ob.display_type = 'TEXTURED'
        bpy.ops.object.select_all(action='INVERT')
        for ob in bpy.context.selected_objects:
            ob.display_type = 'WIRE'
        bpy.ops.object.select_all(action='INVERT')
        return {'FINISHED'}
    
classes = (
    HP_MT_pie_shading,
    HP_OT_shading_wire,
    HP_OT_shading_material,
    HP_OT_shading_solid,
    HP_OT_shading_rendered,
    HP_OT_shading_bg_wire
)
register, unregister = bpy.utils.register_classes_factory(classes)


if __name__ == "__main__":
    register()
