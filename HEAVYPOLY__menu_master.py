import bpy
import random
from bpy.props import *
from bpy_extras.node_utils import find_node_input


class HP_MT_popup_uber(bpy.types.Menu): 
    bl_label = "Heavypoly Uber Popup"
    type: bpy.props.StringProperty(name="Type")

    def draw(self, context):
        layout = self.layout
        # pie = layout.menu_pie()
        # split = pie.split()
        # row = split.row(align=True)
        
        col = layout.column(align=True)
        layout = layout.menu_pie()
        layout.operator_context = 'INVOKE_REGION_WIN'
        #Left
        layout.operator("transform.rotate")
        #Right
        layout.operator("transform.resize", text="Scale")
        #Bottom
        layout.operator("mesh.smart_bevel", text = 'Bevel')
        #Top
        layout.operator("mesh.hp_extrude", text = 'Extrude')
        #Top Left
        layout.operator("transform.shrink_fatten",text = 'Move')
        #Top Right
        layout.operator("mesh.duplicate_extrude", text = 'Extrude')
        #Bottom Left
        layout.operator('popup.hp_render',text = 'Render Settings')
        #Bottom Right
        def cam_props(cam):
            camdat = cam.data
            scene = context.scene
            rd = scene.render
            col.separator()
            col.prop(scene, "camera", text = '')
            col.separator()
            col.prop(camdat, "type", text = '', expand = False)
            if camdat.type == 'PERSP':
                col.prop(camdat, "lens")
            elif camdat.type == 'ORTHO':
                col.prop(camdat, "ortho_scale")
            elif camdat.type == 'PANO':
                engine = context.engine
                if engine == 'CYCLES':
                    ccam = camdat.cycles
                    col.prop(ccam, "panorama_type")
                    if ccam.panorama_type == 'FISHEYE_EQUIDISTANT':
                        col.prop(ccam, "fisheye_fov")
                    elif ccam.panorama_type == 'FISHEYE_EQUISOLID':
                        col.prop(ccam, "fisheye_lens", text="Lens")
                        col.prop(ccam, "fisheye_fov")
                    elif ccam.panorama_type == 'EQUIRECTANGULAR':
                        sub = col.column(align=True)
                        sub.prop(ccam, "latitude_min", text="Latitute Min")
                        sub.prop(ccam, "latitude_max", text="Max")
                        sub = col.column(align=True)
                        sub.prop(ccam, "longitude_min", text="Longiture Min")
                        sub.prop(ccam, "longitude_max", text="Max")
                elif engine in {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_OPENGL'}:
                    col.prop(camdat, "lens")
            row = col.row()
            row.prop(camdat, "dof_distance", text="Focus Distance")
            row.prop(camdat, "dof_object", text="")

            dof_options = camdat.gpu_dof        
            if context.engine == 'BLENDER_EEVEE':
                row = col.row(align = True)
                row.prop(dof_options, "fstop")
                row.prop(dof_options, "blades")
                row = col.row(align = True)
                row.prop(dof_options, "rotation")
                row.prop(dof_options, "ratio")
            else:
                col.label(text="Viewport")
                col.prop(dof_options, "fstop")
                col.prop(dof_options, "blades")
            #SECOND COLUMN##############################################################
            


            col2.prop(rd, "resolution_x", text="Res X")
            col2.prop(rd, "resolution_y", text="Res Y")
            col2.prop(rd, "resolution_percentage", text="Res %")
            #col2.prop(scene, "frame_current", text="Current Frame")
            row = col2.row(align = True)
            row.prop(scene, "frame_start", text="F Start")
            row.prop(scene, "frame_end", text="F End")
            row = col2.row(align = True)
            row.prop(scene, "frame_step", text="Step")
            row.prop(rd, "fps", text = 'FPS')
            
            row = col2.row(align = True)
            row.prop(actdat, "clip_start", text="Clip Start")
            row.prop(actdat, "clip_end", text="Clip End")
        # if bpy.context.space_data.region_3d.view_perspective == 'CAMERA':
            # cam_props(bpy.context.scene.camera)  

        if ob.type == 'CAMERA':
            col.prop(ob, 'name', text = '')
            col.separator()
            cam_props(ob)
        else:
            col.label(text='EMPTY PROPERTIES')
            col.prop(ob, 'name', text = '')
            col.prop(ob, "empty_display_size", text='Display Size')
            col.prop(ob, "empty_display_type", text='')
            

classes = (
    HP_MT_popup_uber,

)
register, unregister = bpy.utils.register_classes_factory(classes)


if __name__ == "__main__":
    register()