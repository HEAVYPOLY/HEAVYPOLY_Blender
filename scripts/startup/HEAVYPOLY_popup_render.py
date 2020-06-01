import bpy
import random
from bpy.props import *
from bpy_extras.node_utils import find_node_input

class HP_MT_popup_render(bpy.types.Operator):
    bl_idname = "popup.hp_render" 
    bl_label = "Heavypoly Render Popup"
    def execute(self, context):
        return {'FINISHED'}
 
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self, width=450)
        
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = row.column()
        col2 = row.column()
        layout.use_property_split = True
#FIRST COLUMN##############################################################

        scene = context.scene
        rd = scene.render
        props = scene.eevee
        image_settings = rd.image_settings
        col.label(text='RENDER CAMERA')
        col.prop(scene, "camera", text = '')
        row = col.row()
        row.scale_x=.5
        row.prop(rd, "resolution_x", text="X")
        row.prop(rd, "resolution_y", text="Y")
        row.prop(rd, "resolution_percentage", text="%")
        row = col.row()
        row.prop(scene, "frame_start", text="F Start")
        row.prop(rd, "fps", text = 'F Rate')
        row = col.row()
        row.prop(scene, "frame_end", text="F End")
        row.prop(scene, "frame_step", text="F Step")
        col.separator()
        row = col.row()
        row.operator('render.opengl',text='R View')
        row.operator('render.render',text='R Cam')
        row = col.row()
        row.operator('render.opengl',text='R View Anim').animation=True
        row.operator('render.render',text='R Cam Anim').animation=True
        col.separator()

#           col.prop(world, "use_nodes", icon='NODETREE')

        col.label(text='WORLD')
        world = bpy.context.scene.world
        col.prop(scene.eevee, "use_soft_shadows")
        if world.use_nodes:
            ntree = world.node_tree
            node = ntree.get_output_node('EEVEE')

        
        
            if node:
                input = find_node_input(node, 'Surface')
                inputvol = find_node_input(node, 'Volume')
                if input:
                    col.template_node_view(ntree, node, input)
                if input:
                    col.separator()
                    col.separator()
                    col.prop(scene.eevee, "use_volumetric", text="Use Volumetric")
                    col.template_node_view(ntree, node, inputvol)
                else:
                    col.label(text="Incompatible output node")
            else:
                col.label(text="No output node")
        else:
            col.prop(world, "color")
        scene = bpy.context.scene
        props = scene.eevee
        # col.label(text='BLOOM')
        # box = col.box().column()
        # box.active = props.use_bloom
        # box.prop(props, "bloom_threshold")
        # box.prop(props, "bloom_knee")
        # box.prop(props, "bloom_radius")
        # box.prop(props, "bloom_color")
        # box.prop(props, "bloom_intensity")
        # box.prop(props, "bloom_clamp")
#SECOND COLUMN##############################################################

                
        

      
        col2.label(text='RENDER SETTINGS')
        col2.prop(scene.render, "engine",text='')
        col2.prop(scene.view_settings, 'view_transform', text='')
        col2.prop(scene.view_settings, 'look', text='')
        col2.template_curve_mapping(scene.view_settings, "curve_mapping", levels=True)
        col2.prop(image_settings, "file_format", text = '')
        col2.prop(image_settings, "compression")
        row = col2.row()
        row.scale_x=.5
        if image_settings.file_format == 'FFMPEG':
            row.prop(rd.ffmpeg, "format", text= '')
            row.prop(rd.ffmpeg, "codec",text='')
            
        else:
            row = col2.row()
            row.scale_x=.2
            row.prop(image_settings, "color_mode", expand = True)
            row = col.row()
            row.scale_x=.2
            row.prop(image_settings, "col_depth", expand = True)
        col2.prop(rd, "filepath", text="")
        col2.prop(rd, "use_overwrite")
#       col.prop(rd, "use_placeholder")

#       col.prop(rd, "use_file_extension")
#       col.prop(rd, "use_render_cache")
        ffmpeg = rd.ffmpeg
        col2.prop(props, "taa_samples")
        col2.prop(props, "taa_render_samples")
        col2.prop(props, "use_taa_reprojection")

classes = (
    HP_MT_popup_render,

)
register, unregister = bpy.utils.register_classes_factory(classes)


if __name__ == "__main__":
    register()