import bpy
import random
from bpy.props import *
from bpy_extras.node_utils import find_node_input

#class HP_PT_transforms(bpy.types.Panel):
#    bl_label = "HEAVYPOLY TRANSFORM"
#    bl_space_type = 'PROPERTIES'
#    bl_region_type = 'WINDOW'
#    bl_context = "object"

#    def draw(self, context):
#        layout = self.layout
#        layout.use_property_split = False

#        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

#        ob = context.object

#        col = flow.column()
#        row = col.row(align=True)
#        row.prop(ob, "location")
#        row.use_property_decorate = False
#        row.prop(ob, "lock_location", text="", emboss=False, icon='DECORATE_UNLOCKED')

#        rotation_mode = ob.rotation_mode
#        
#        layout.use_property_split = True
#        col = flow.column()
#        row = col.row(align=True)
#        row.prop(ob, "rotation_euler", text="Rotation")
#        row.use_property_decorate = False
#        row.prop(ob, "lock_rotation", text="", emboss=False, icon='DECORATE_UNLOCKED')

#        col = flow.column()
#        row = col.row(align=True)
#        row.prop(ob, "scale")
#        row.use_property_decorate = False
#        row.prop(ob, "lock_scale", text="", emboss=False, icon='DECORATE_UNLOCKED')

class HP_PT_object_properties(bpy.types.Panel):
    bl_label = "HEAVYPOLY PROPERTIES"
    bl_idname = "OBJECT_PT_hp_object_properties"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
        
    def draw(self, context):
        layout = self.layout
        ob = bpy.context.object

            
        row = layout.row()
        col = row.column(align=True)
        col2 = row.column()
        try:
            actdat = bpy.context.active_object.data
        except:
            pass

        def cam_props(cam):
            camdat = cam.data
            scene = bpy.context.scene
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

            dof_options = camdat.dof        
            if context.engine == 'BLENDER_EEVEE':
                row = col.row(align = True)
                row.prop(dof_options, "aperture_fstop")
                row.prop(dof_options, "aperture_blades")
                row = col.row(align = True)
                row.prop(dof_options, "focus_distance")
                row.prop(dof_options, "focus_object", text = "")
 
            else:
                col.label(text="Viewport")
                col.prop(dof_options, "aperture_fstop")
                col.prop(dof_options, "aperture_blades")
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
            
            #row = col2.row(align = True)
            #row.prop(actdat, "clip_start", text="Clip Start")
            #row.prop(actdat, "clip_end", text="Clip End")
        # if bpy.context.space_data.region_3d.view_perspective == 'CAMERA':
            # cam_props(bpy.context.scene.camera)  

        if ob.type == 'CAMERA':
            cam_props(ob)
        elif ob.type == 'EMPTY':
            col.prop(ob, "empty_display_size", text='Display Size')
            col.prop(ob, "empty_display_type", text='')
            

        elif ob.type == 'LIGHT':
            col.label(text='Light Type')
            col.prop(actdat, "type", text = '', expand = False)
            if actdat.type in {'POINT', 'SPOT', 'SUN'}:
                col.prop(actdat, "shadow_soft_size", text="Radius")
            if actdat.type == 'AREA':
                col.prop(actdat, "shape", text='')
                if actdat.shape in {'SQUARE', 'DISK'}:
                    col.prop(actdat, "size")
                if actdat.shape in {'RECTANGLE', 'ELLIPSE'}:
                    col.prop(actdat, "size", text="Size X")
                    col.prop(actdat, "size_y", text="Size Y")
            if actdat.type == 'SUN':                
                col.prop(actdat, "shadow_cascade_count", text="Count")
                col.prop(actdat, "shadow_cascade_fade", text="Fade")
                col.prop(actdat, "shadow_cascade_max_distance", text="Max Distance")
                col.prop(actdat, "shadow_cascade_exponent", text="Distribution")
            if actdat.type == 'SPOT':
                col.prop(actdat, "spot_size", text="Size")
                col.prop(actdat, "spot_blend", text="Blend", slider=True)
                col.prop(actdat, "show_cone")
            col.prop(actdat, "color")
            col.prop(actdat, "energy")
            col2.label(text='Shadows')
            col2.prop(actdat, "shadow_buffer_clip_start", text="Clip Start")
            # col2.prop(actdat, "shadow_buffer_clip_end", text="End")
            # col2.prop(actdat, "shadow_buffer_soft", text="Fake Softness")
            col2.prop(actdat, "shadow_buffer_bias", text="Contact Clip")
            # col2.prop(actdat, "shadow_buffer_exp", text="Darkness")
            # col2.prop(actdat, "shadow_buffer_bleed_bias", text="Bleed Bias")
            col2.prop(actdat, "cutoff_distance", text="Distance")
            scene = context.scene
            props = scene.eevee
            
            col.label(text='GLOBAL LIGHT PROPERTIES')
            row=col2.row()
            row.scale_x=.2
            #row.prop(props, "shadow_method", text='')
            row.prop(props, "shadow_cube_size", text="")
            row.prop(props, "shadow_cascade_size", text="")
            col.prop(props, "use_shadow_high_bitdepth")
            col.prop(props, "use_soft_shadows")
            col.prop(props, "taa_samples")
            col.prop(props, "taa_render_samples")

 
        elif ob.type == 'LIGHT_PROBE':
            col.label(text='LIGHT PROBE PROPERTIES')
            col.prop(bpy.context.active_object, 'name', text = '')
            probe = actdat
            if probe.type == 'GRID':
                col.prop(probe, "influence_distance", text="Distance")
                col.prop(probe, "falloff")
                col.prop(probe, "intensity")
                col.separator()
                col.prop(probe, "grid_resolution_x", text="Grid X")
                col.prop(probe, "grid_resolution_y", text="Grid Y")
                col.prop(probe, "grid_resolution_z", text="Grid Z")
            elif probe.type == 'PLANAR':
                col.prop(probe, "influence_distance", text="Distance")
            else:
                col.prop(probe, "influence_type")
                if probe.influence_type == 'ELIPSOID':
                    col.prop(probe, "influence_distance", text="Radius")
                else:
                    col.prop(probe, "influence_distance", text="Size")
                col.prop(probe, "falloff")
                col.prop(probe, "intensity")
            col2.operator('scene.light_cache_bake')
            col2.operator('scene.light_cache_free')
            

        elif ob.type == 'MESH':
            if bpy.context.object.mode == 'SCULPT':
                toolsettings = bpy.context.tool_settings
                sculpt = toolsettings.sculpt
                
                brush = toolsettings.unified_paint_settings
                col.label(text='SCULPT PROPERTIES')         
                col.prop(bpy.context.active_object, 'name', text = '')
                col.separator()
                col.prop(brush, "size")

                row = col.row()
                sub = row.column()
                sub.scale_x=.1

                sub.operator('paint.brush_select',text = 'Snake Hook').sculpt_tool='SNAKE_HOOK'
                sub.operator('paint.brush_select',text = 'Inflate').sculpt_tool='INFLATE'
                sub.operator('paint.brush_select',text = 'Crease').sculpt_tool='CREASE'
                sub.operator('paint.brush_select',text = 'Clay').sculpt_tool='CLAY'
                sub = row.column()
                sub.scale_x=.1
                sub.operator('paint.brush_select',text = 'Draw').sculpt_tool='DRAW'
                sub.operator('paint.brush_select',text = 'Grab').sculpt_tool='GRAB'
                sub.operator('paint.brush_select',text = 'Flatten').sculpt_tool='FLATTEN'
                sub.operator('paint.brush_select',text = 'Fill').sculpt_tool='FILL'
#               col.operator('sculpt.dynamic_topology_toggle', text = 'Dynotopo')
                row = col.row()
                row.prop(sculpt.brush, "use_frontface")
                row.prop(sculpt, "use_symmetry_x")
                row.prop(sculpt, "use_smooth_shading")
                row = col.row()
                if sculpt.detail_type_method in {'CONSTANT','MANUAL'}:
                    row.prop(sculpt, "constant_detail_resolution")
                if sculpt.detail_type_method == 'BRUSH':
                    row.prop(sculpt, "detail_percent")
                if sculpt.detail_type_method == 'RELATIVE':
                    row.prop(sculpt, "detail_size")
                #col.prop(sculpt, "detail_refine_method",text='')
                row.prop(sculpt, "detail_type_method",text='')
                row = col.row()
                row.operator("sculpt.detail_flood_fill",text='Detail Flood Fill')
                row.operator(
                    "sculpt.dynamic_topology_toggle",
                    icon='CHECKBOX_HLT' if bpy.context.sculpt_object.use_dynamic_topology_sculpting else 'CHECKBOX_DEHLT',
                    text="Dynotopo",
                )
   
                
                #bpy.ops.wm.tool_set_by_id(name="Draw", space_type = 'VIEW_3D')
#            else:
#                col.operator_menu_enum("object.modifier_add", "type")
#                for md in ob.modifiers:
#                    box = col.template_modifier(md)
#                    if box:
#                        getattr(self, md.type)(box, ob, md)


            ##SECOND COLUMN##############################################################


                            
        elif ob.type == 'GPENCIL':            
            toolsettings = bpy.context.tool_settings
            sculpt = toolsettings.sculpt

            brush = toolsettings.unified_paint_settings
            col.separator()
            col.prop(toolsettings.gpencil_paint.brush, "size")

            row = col.row()
            sub = row.column()
            sub.scale_x=.1
            sub2 = row.column()
            sub2.scale_x=.1
            sub.operator('wm.tool_set_by_id',text = 'Draw').name='builtin_brush.Draw'
            sub.operator('wm.tool_set_by_id',text = 'Erase').name='builtin_brush.Erase'
            sub.operator('wm.tool_set_by_id',text = 'Fill').name='builtin_brush.Fill'
            sub2.operator('wm.tool_set_by_id',text = 'Box').name='builtin.box'
            sub2.operator('wm.tool_set_by_id',text = 'Circle').name='builtin.circle'
            sub2.operator('wm.tool_set_by_id',text = 'Line').name='builtin.line'
            col.prop(bpy.context.tool_settings.gpencil_sculpt, "lock_axis", text = '')
            col.prop(bpy.context.tool_settings, "gpencil_stroke_placement_view3d", text = '')

            col2.operator_menu_enum("object.gpencil_modifier_add", "type")
            for md in ob.grease_pencil_modifiers:
                box = col2.template_greasepencil_modifier(md)
                if box:
                    getattr(self, md.type)(box, ob, md)                 

        elif ob.type == 'META':
            col2.label(text='META PROPERTIES')
            col.prop(bpy.context.active_object, 'name', text = '')
            try:
                col.prop(actdat.elements.active, "type", text='')
                col.prop(actdat.elements.active, "radius", text = 'Size')
                if actdat.elements.active.type == 'CAPSULE':
                    col.prop(actdat.elements.active, "size_x", text = 'X')
                if actdat.elements.active.type == 'PLANE':
                    col.prop(actdat.elements.active, "size_x", text = 'X')
                    col.prop(actdat.elements.active, "size_y", text = 'Y')          
                if actdat.elements.active.type in {'CUBE','ELLIPSOID'}:
                    col.prop(actdat.elements.active, "size_x", text = 'X')
                    col.prop(actdat.elements.active, "size_y", text = 'Y')
                    col.prop(actdat.elements.active, "size_z", text = 'Z')
                col.prop(actdat.elements.active, "stiffness", text = 'Stiffness')
                col.prop(actdat.elements.active, "use_negative", text = 'Subtract')
                col.prop(actdat.elements.active, "hide", text = 'Hide')
            
            except:
                pass
            col2.prop(actdat, "resolution", text = 'Resolution')
            col2.prop(actdat, "render_resolution", text = 'Render Resolution')
            col2.prop(actdat, "threshold")
            col2.label(text='Update Method')
            col2.prop(actdat, "update_method", text = '')
            col2.operator('object.convert', text= 'Convert To Mesh').target = 'MESH'
            
        elif ob.type == 'LATTICE':
            col.label(text='LATTICE PROPERTIES')
            col.prop(bpy.context.active_object, 'name', text = '')
            col.separator()
            lat = actdat
            col = col.column(align=True)
            col.prop(lat, "points_u", text="U")
            col.prop(lat, "points_v", text="V")
            col.prop(lat, "points_w", text="W")
            col.separator()
            col.prop(lat, "interpolation_type_u", text="U")
            col.prop(lat, "interpolation_type_v", text="V")
            col.prop(lat, "interpolation_type_w", text="W")
            col.prop(lat, "use_outside")
            col.prop_search(lat, "vertex_group", context.object, "vertex_groups")

        elif ob.type == 'FONT':
            text = actdat
            col.label(text='TEXT PROPERTIES')
            col.prop(bpy.context.active_object, 'name', text = '')
            char = text.edit_format
#           row = layout.split(factor=0.25)
#           row.label(text="Regular")
            col.template_ID(text, "font", open="font.open", unlink="font.unlink")
            # row = layout.split(factor=0.25)
            # row.label(text="Bold")
            # row.template_ID(text, "font_bold", open="font.open", unlink="font.unlink")
            # row = layout.split(factor=0.25)
            # row.label(text="Italic")
            # row.template_ID(text, "font_italic", open="font.open", unlink="font.unlink")
            # row = layout.split(factor=0.25)
            # row.label(text="Bold & Italic")
            # row.template_ID(text, "font_bold_italic", open="font.open", unlink="font.unlink")
            # row = layout.row(align=True)
            # row.prop(char, "use_bold", toggle=True)
            # row.prop(char, "use_italic", toggle=True)
            # row.prop(char, "use_underline", toggle=True)
            # row.prop(char, "use_small_caps", toggle=True)         

            col.prop(text, "size", text="Size")
            col.prop(text, "shear")
            col.prop(text, "space_character", text="Character Spacing")
            col.prop(text, "space_word", text="Word Spacing")
            col.prop(text, "space_line", text="Line Spacing")

#           col.prop(text, "family")
            
            # sub = col.column(align=True)
            # sub.prop(text, "underline_position", text="Underline Position")
            # sub.prop(text, "underline_height", text="Underline Thickness")
            # col.prop(text, "small_caps_scale", text="Small Caps Scale")
            col.prop(text, "align_x", text="")
            col.prop(text, "align_y", text="")
            col.prop(text, "offset_x", text="Offset X")
            col.prop(text, "offset_y", text="Offset Y")
            col.prop(text, "follow_curve")
            
            col2.label(text='3D TEXT PROPERTIES')
            col2.prop(text, "offset")
            col2.prop(text, "extrude")
            col2.prop(text, "taper_object")
            col2.prop(text, "use_map_taper")
            col2.operator('object.convert', text = 'Convert to Curves').target = 'CURVE'
            col2.operator('object.convert', text = 'Convert to Mesh').target = 'MESH'

            
        elif ob.type == 'CURVE':    
            col.label(text='CURVE PROPERTIES')
            col.prop(bpy.context.active_object, 'name', text = '')
            
            curve = actdat
            col.label(text='Extrusion Shape')
            col.prop(curve, "fill_mode", text='')
            col.prop(curve, "bevel_object", text="")
            col.prop(curve, "bevel_depth", text="Thickness")
            col.prop(curve, "bevel_resolution", text="Smoothness")
            col.prop(curve, "offset")
            col.prop(curve, "extrude")
            col.prop(curve, "use_map_taper")
            col.prop(curve, "use_fill_caps")
            col.prop(curve, "taper_object", text='')
            row = col.row(align=True)
            row.scale_x=.1
            row.prop(curve, "dimensions", expand=True)
            col2.prop(curve, "resolution_u", text="Resolution U")
            col2.prop(curve, "resolution_v", text="Resolution V")
            col2.prop(curve, "render_resolution_u", text="Render U")
            col2.prop(curve, "render_resolution_v", text="Render V")
            col2.prop(curve, "twist_mode")
            col2.prop(curve, "twist_smooth", text="Smooth")

            col2.prop(curve, "use_fill_deform")
            col2.prop(curve, "use_radius")
            col2.prop(curve, "use_stretch")
            col2.prop(curve, "use_deform_bounds")
            col2.prop(curve, "bevel_factor_start", text="Bevel Start")
            col2.prop(curve, "bevel_factor_end", text="End")
            col2.prop(curve, "bevel_factor_mapping_start", text="Bevel Mapping Start")
            col2.prop(curve, "bevel_factor_mapping_end", text="End")

           
        elif len(bpy.context.selected_objects) == 0 or self.type == 'WORLD':
            col.label(text='WORLD PROPERTIES')
            if bpy.context.scene.camera:
                cam_props(bpy.context.scene.camera)
            
            world = bpy.context.scene.world
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
                        col.template_node_view(ntree, node, inputvol)
                    else:
                        col.label(text="Incompatible output node")
                else:
                    col.label(text="No output node")
            else:
                col.prop(world, "color")
            scene = bpy.context.scene
            props = scene.eevee
            box = col.box().column()
            
            box.active = props.use_bloom
            box.label(text = 'Bloom')
            box.prop(props, "bloom_threshold")
            box.prop(props, "bloom_knee")
            box.prop(props, "bloom_radius")
            box.prop(props, "bloom_color")
            box.prop(props, "bloom_intensity")
            box.prop(props, "bloom_clamp")
            scene = context.scene
            rd = scene.render
            row = col2.row(align = True)
            row.prop(actdat, "clip_start", text="Clip Start")
            row.prop(actdat, "clip_end", text="Clip End")
            
            col2.prop(bpy.context.scene.render, "engine",text='')
            col2.prop(bpy.context.scene.view_settings, 'view_transform', text='')
            col2.prop(bpy.context.scene.view_settings, 'look', text='')

            col2.template_curve_mapping(bpy.context.scene.view_settings, "curve_mapping", type='COLOR', levels=True)
        
classes = (
    HP_PT_object_properties,
#    HP_PT_transforms

)
register, unregister = bpy.utils.register_classes_factory(classes)


if __name__ == "__main__":
    register()
