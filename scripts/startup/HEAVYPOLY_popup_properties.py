import bpy
import random
from bpy.props import *
from bpy_extras.node_utils import find_node_input


class HP_MT_popup_properties(bpy.types.Operator):
    bl_idname = "popup.hp_properties"
    bl_label = "Heavypoly Properties Popup"
    type: bpy.props.StringProperty(name="Type")
    mode: bpy.props.StringProperty(name="Mode")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        ob = context.object
        wm = context.window_manager
        return wm.invoke_popup(self, width=350)

    def draw(self, context):
        layout = self.layout


        row = layout.row()
        col = row.column(align=True)
        col2 = row.column()
        if self.mode == 'Draw':
            col.label(text='DRAW PROPERTIES')


        col.operator('popup.hp_render',text = 'Render Settings')
        try:
            ob = context.object
            actdat = bpy.context.active_object.data
        except:
            pass

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

            row = col2.row(align = True)
            row.prop(actdat, "clip_start", text="Clip Start")
            row.prop(actdat, "clip_end", text="Clip End")
        # if bpy.context.space_data.region_3d.view_perspective == 'CAMERA':
            # cam_props(bpy.context.scene.camera)

        if ob.type == 'CAMERA':
            col.prop(ob, 'name', text = '')
            col.separator()
            cam_props(ob)
        elif ob.type == 'EMPTY':
            col.label(text='EMPTY PROPERTIES')
            col.prop(ob, 'name', text = '')
            col.prop(ob, "empty_display_size", text='Display Size')
            col.prop(ob, "empty_display_type", text='')


        elif len(bpy.context.selected_objects) == 0 or self.type == 'WORLD':
            if bpy.context.scene.camera:
                cam_props(bpy.context.scene.camera)

            col.label(text='WORLD PROPERTIES')
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
            # row.prop(actdat, "clip_start", text="Clip Start")
            # row.prop(actdat, "clip_end", text="Clip End")

            col2.prop(bpy.context.scene.render, "engine",text='')
            col2.prop(bpy.context.scene.view_settings, 'view_transform', text='')
            col2.prop(bpy.context.scene.view_settings, 'look', text='')

            col2.template_curve_mapping(bpy.context.scene.view_settings, "curve_mapping", type='COLOR', levels=True)



        elif ob.type == 'LIGHT':
            col.label(text='LIGHT PROPERTIES')
            col.prop(bpy.context.active_object, 'name', text = '')
            col.label(text='Light Type')
            col.prop(actdat, "type", text = '', expand = False)
            col.prop(actdat, "color")
            col.prop(actdat, "energy")
            if actdat.type in {'POINT', 'SPOT', 'SUN'}:
                col.prop(actdat, "shadow_soft_size", text="Radius")
            if actdat.type == 'AREA':
                col.separator()
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
            col.label(text='Shadows')
            col.prop(actdat, "shadow_buffer_clip_start", text="Clip Start")
            col.prop(actdat, "shadow_buffer_bias", text="Bias")
            col.prop(actdat, "cutoff_distance", text="Distance")

            # col.prop(actdat, "use_contact_shadow", text="Use Contact Shadows")
            # col.prop(actdat, "contact_shadow_distance", text="Distance")
            # col.prop(actdat, "contact_shadow_soft_size", text="Softness")
            # col.prop(actdat, "contact_shadow_bias", text="Bias")
            # col.prop(actdat, "contact_shadow_thickness", text="Thickness")
            scene = context.scene
            props = scene.eevee

            col2.label(text='GLOBAL LIGHT PROPERTIES')
            row=col2.row()
            row.scale_x=.2
            # row.prop(props, "shadow_method", text='')
            row.prop(props, "shadow_cube_size", text="")
            row.prop(props, "shadow_cascade_size", text="")
            col2.prop(props, "use_shadow_high_bitdepth")
            col2.prop(props, "use_soft_shadows")
            col2.prop(props, "taa_samples")
            col2.prop(props, "taa_render_samples")

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
                sub2 = row.column()
                sub2.scale_x=.1

                sub.operator('wm.tool_set_by_id',text = 'Draw').name='builtin_brush.Draw'
                sub.operator('wm.tool_set_by_id',text = 'Inflate').name='builtin_brush.Inflate'
                sub.operator('wm.tool_set_by_id',text = 'Flatten').name='builtin_brush.Flatten'
                sub.operator('wm.tool_set_by_id',text = 'Crease').name='builtin_brush.Crease'
                sub2.operator('wm.tool_set_by_id',text = 'Clay').name='builtin_brush.Clay'
                sub2.operator('wm.tool_set_by_id',text = 'Fill').name='builtin_brush.Fill'
                sub2.operator('wm.tool_set_by_id',text = 'Grab').name='builtin_brush.Grab'
                sub2.operator('wm.tool_set_by_id',text = 'Snake Hook').name='builtin_brush.Snake Hook'
#               col.operator('sculpt.dynamic_topology_toggle', text = 'Dynotopo')
                col.prop(sculpt.brush, "use_frontface")
                if sculpt.detail_type_method in {'CONSTANT','MANUAL'}:
                    col.prop(sculpt, "constant_detail_resolution")
                if sculpt.detail_type_method == 'BRUSH':
                    col.prop(sculpt, "detail_percent")
                if sculpt.detail_type_method == 'RELATIVE':
                    col.prop(sculpt, "detail_size")
                #col.prop(sculpt, "detail_refine_method",text='')
                col.prop(sculpt, "detail_type_method",text='')
                col.operator("sculpt.detail_flood_fill",text='Detail Flood Fill')
                col.operator(
                    "sculpt.dynamic_topology_toggle",
                    icon='CHECKBOX_HLT' if bpy.context.sculpt_object.use_dynamic_topology_sculpting else 'CHECKBOX_DEHLT',
                    text="Dynotopo",
                )

                col.prop(sculpt, "use_symmetry_x")

                #bpy.ops.wm.tool_set_by_id(name="Draw", space_type = 'VIEW_3D')
            else:
                col.scale_x = 0.7
                col.label(text='MESH PROPERTIES')
                col.prop(bpy.context.active_object, 'name', text = '')

                col.separator()
                ob = context.object
                group = ob.vertex_groups.active
                rows = 3
                row = col.row(align=True)
                row2 = col.row(align=True)
                sub = row.row(align=True)

                sub.template_list("MESH_UL_vgroups", "", ob, "vertex_groups", ob.vertex_groups, "active_index", rows=rows)
                sub = row.column(align=True)
                sub.scale_x = 0.3
                sub.operator("object.vertex_group_add", icon='ADD', text="")
                sub.operator("object.vertex_group_remove", icon='REMOVE', text="")
                sub.operator("object.vertex_group_assign", text="A")
                sub.operator("object.vertex_group_remove_from", text="R")
                subcol = row2.column(align=True)
                subcol.scale_x = 0.5
                subcol.prop(ob, "location", text="Location")
                subcol.prop(ob, "rotation_euler", text="Rotation")
                subcol = row2.column(align=True)
                subcol.scale_x = 0.5
                subcol.prop(ob, "scale")
                subcol.prop(ob, "dimensions")
                col.use_property_decorate = False
                
                col.prop(bpy.context.active_object.data, "auto_smooth_angle")
            ##SECOND COLUMN##############################################################

            col2.label(text='MODIFIERS')
            col2.operator_menu_enum("object.modifier_add", "type")
            for md in ob.modifiers:
                        box = col2.template_modifier(md)
                        if box:
                            getattr(self, md.type)(box, ob, md)

        elif ob.type == 'GPENCIL':
            col.label(text='GREASE PENCIL PROPERTIES')
            col.prop(bpy.context.active_object, 'name', text = '')

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

            # col.operator('view3d.gp_canvas', text = 'Side', icon='NONE').type = 'X'
            # col.operator('view3d.gp_canvas', text = 'Front', icon='NONE').type = 'Y'
            # col.operator('view3d.gp_canvas', text = 'Top', icon='NONE').type = 'Z'

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
            col2.prop(curve, "use_fast_edit", text="Fast Editing")

            col2.prop(curve, "use_fill_deform")
            col2.prop(curve, "use_radius")
            col2.prop(curve, "use_stretch")
            col2.prop(curve, "use_deform_bounds")
            col2.prop(curve, "bevel_factor_start", text="Bevel Start")
            col2.prop(curve, "bevel_factor_end", text="End")
            col2.prop(curve, "bevel_factor_mapping_start", text="Bevel Mapping Start")
            col2.prop(curve, "bevel_factor_mapping_end", text="End")
###GP Modifiers

    def GP_NOISE(self, layout, ob, md):
        gpd = ob.data
        split = layout.split()

        col = split.column()
        row = col.row(align=True)
        row.prop(md, "factor")
        row.prop(md, "random", text="", icon='TIME', toggle=True)
        row = col.row()
        row.enabled = md.random
        row.prop(md, "step")
        col.prop(md, "full_stroke")
        col.prop(md, "move_extreme")

        row = layout.row(align=True)
        row.label(text="Affect:")
        row = layout.row(align=True)
        row.prop(md, "use_edit_position", text="Position", icon='MESH_DATA', toggle=True)
        row.prop(md, "use_edit_strength", text="Strength", icon='COLOR', toggle=True)
        row.prop(md, "use_edit_thickness", text="Thickness", icon='LINE_DATA', toggle=True)
        row.prop(md, "use_edit_uv", text="UV", icon='MOD_UVPROJECT', toggle=True)

        col = layout.column()
        col.separator()
        col.label(text="Vertex Group:")
        row = col.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        row.prop(md, "invert_vertex", text="", icon='ARROW_LEFTRIGHT')

        col.label(text="Material:")
        row = col.row(align=True)
        row.prop(md, "pass_index", text="Pass")
        row.prop(md, "invert_material_pass", text="", icon='ARROW_LEFTRIGHT')

        col.label(text="Layer:")
        row = col.row(align=True)
        row.prop_search(md, "layer", gpd, "layers", text="", icon='GREASEPENCIL')
        row.prop(md, "invert_layers", text="", icon='ARROW_LEFTRIGHT')
        row = layout.row(align=True)
        row.prop(md, "layer_pass", text="Pass")
        row.prop(md, "invert_layer_pass", text="", icon='ARROW_LEFTRIGHT')

    def GP_SMOOTH(self, layout, ob, md):
        gpd = ob.data
        col = layout.column()
        col.prop(md, "factor")
        col.prop(md, "step")

        col.label(text="Affect:")
        row = col.row(align=True)
        row.prop(md, "use_edit_position", text="Position", icon='MESH_DATA', toggle=True)
        row.prop(md, "use_edit_strength", text="Strength", icon='COLOR', toggle=True)
        row.prop(md, "use_edit_thickness", text="Thickness", icon='LINE_DATA', toggle=True)
        row.prop(md, "use_edit_uv", text="UV", icon='MOD_UVPROJECT', toggle=True)

        col.separator()
        col.label(text="Vertex Group:")
        row = col.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        row.prop(md, "invert_vertex", text="", icon='ARROW_LEFTRIGHT')

        col.label(text="Material:")
        row = col.row(align=True)
        row.prop(md, "pass_index", text="Pass")
        row.prop(md, "invert_material_pass", text="", icon='ARROW_LEFTRIGHT')

        col.label(text="Layer:")
        row = col.row(align=True)
        row.prop_search(md, "layer", gpd, "layers", text="", icon='GREASEPENCIL')
        row.prop(md, "invert_layers", text="", icon='ARROW_LEFTRIGHT')
        row = layout.row(align=True)
        row.prop(md, "layer_pass", text="Pass")
        row.prop(md, "invert_layer_pass", text="", icon='ARROW_LEFTRIGHT')

    def GP_SUBDIV(self, layout, ob, md):
        gpd = ob.data
        split = layout.split()

        col = split.column()
        row = col.row(align=True)
        row.prop(md, "level")
        row.prop(md, "simple", text="", icon='PARTICLE_POINT')

        col = layout.column()
        col.separator()
        col.label(text="Material:")
        row = col.row(align=True)
        row.prop(md, "pass_index", text="Pass")
        row.prop(md, "invert_material_pass", text="", icon='ARROW_LEFTRIGHT')

        col.label(text="Layer:")
        row = col.row(align=True)
        row.prop_search(md, "layer", gpd, "layers", text="", icon='GREASEPENCIL')
        row.prop(md, "invert_layers", text="", icon='ARROW_LEFTRIGHT')
        row = layout.row(align=True)
        row.prop(md, "layer_pass", text="Pass")
        row.prop(md, "invert_layer_pass", text="", icon='ARROW_LEFTRIGHT')

    def GP_SIMPLIFY(self, layout, ob, md):
        gpd = ob.data

        row = layout.row()
        row.prop(md, "mode")

        split = layout.split()

        col = split.column()
        col.label(text="Settings:")
        row = col.row(align=True)
        row.enabled = md.mode == 'FIXED'
        row.prop(md, "step")

        row = col.row(align=True)
        row.enabled = not md.mode == 'FIXED'
        row.prop(md, "factor")

        col = layout.column()
        col.separator()
        col.label(text="Material:")
        row = col.row(align=True)
        row.prop(md, "pass_index", text="Pass")
        row.prop(md, "invert_material_pass", text="", icon='ARROW_LEFTRIGHT')

        col.label(text="Layer:")
        row = col.row(align=True)
        row.prop_search(md, "layer", gpd, "layers", text="", icon='GREASEPENCIL')
        row.prop(md, "invert_layers", text="", icon='ARROW_LEFTRIGHT')
        row = layout.row(align=True)
        row.prop(md, "layer_pass", text="Pass")
        row.prop(md, "invert_layer_pass", text="", icon='ARROW_LEFTRIGHT')

    def GP_THICK(self, layout, ob, md):
        gpd = ob.data
        split = layout.split()

        col = split.column()
        row = col.row(align=True)
        row.prop(md, "thickness")

        col.prop(md, "normalize_thickness")

        if not md.normalize_thickness:
            split = layout.split()
            col = split.column()
            col.prop(md, "use_custom_curve")

            if md.use_custom_curve:
                col.template_curve_mapping(md, "curve")

        col = layout.column()
        col.separator()
        col.label(text="Vertex Group:")
        row = col.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        row.prop(md, "invert_vertex", text="", icon='ARROW_LEFTRIGHT')

        col.label(text="Material:")
        row = col.row(align=True)
        row.prop(md, "pass_index", text="Pass")
        row.prop(md, "invert_material_pass", text="", icon='ARROW_LEFTRIGHT')

        col.label(text="Layer:")
        row = col.row(align=True)
        row.prop_search(md, "layer", gpd, "layers", text="", icon='GREASEPENCIL')
        row.prop(md, "invert_layers", text="", icon='ARROW_LEFTRIGHT')
        row = layout.row(align=True)
        row.prop(md, "layer_pass", text="Pass")
        row.prop(md, "invert_layer_pass", text="", icon='ARROW_LEFTRIGHT')

    def GP_TINT(self, layout, ob, md):
        gpd = ob.data
        split = layout.split()

        col = split.column()
        col.prop(md, "color")
        col.prop(md, "factor")

        row = layout.row()
        row.prop(md, "create_materials")
        row.prop(md, "modify_color")

        col = layout.column()
        col.separator()
        col.label(text="Material:")
        row = col.row(align=True)
        row.prop(md, "pass_index", text="Pass")
        row.prop(md, "invert_material_pass", text="", icon='ARROW_LEFTRIGHT')

        col.label(text="Layer:")
        row = col.row(align=True)
        row.prop_search(md, "layer", gpd, "layers", text="", icon='GREASEPENCIL')
        row.prop(md, "invert_layers", text="", icon='ARROW_LEFTRIGHT')
        row = layout.row(align=True)
        row.prop(md, "layer_pass", text="Pass")
        row.prop(md, "invert_layer_pass", text="", icon='ARROW_LEFTRIGHT')

    def GP_TIME(self, layout, ob, md):
        gpd = ob.data

        row = layout.row()
        row.prop(md, "mode", text="Mode")

        row = layout.row()
        if md.mode == 'FIX':
            txt = "Frame"
        else:
            txt = "Frame Offset"
        row.prop(md, "offset", text=txt)

        row = layout.row()
        row.enabled = md.mode != 'FIX'
        row.prop(md, "frame_scale")

        row = layout.row()
        row.enabled = md.mode != 'FIX'
        row.prop(md, "use_keep_loop")

        row = layout.row()
        row.label(text="Layer:")
        row = layout.row(align=True)
        row.prop_search(md, "layer", gpd, "layers", text="", icon='GREASEPENCIL')
        row.prop(md, "invert_layers", text="", icon='ARROW_LEFTRIGHT')

        row = layout.row(align=True)
        row.prop(md, "layer_pass", text="Pass")
        row.prop(md, "invert_layer_pass", text="", icon='ARROW_LEFTRIGHT')

    def GP_COLOR(self, layout, ob, md):
        gpd = ob.data
        split = layout.split()

        col = split.column()
        col.label(text="Color:")
        col.prop(md, "hue", text="H")
        col.prop(md, "saturation", text="S")
        col.prop(md, "value", text="V")

        row = layout.row()
        row.prop(md, "create_materials")
        row.prop(md, "modify_color")

        col = layout.column()
        col.separator()
        col.label(text="Material:")
        row = col.row(align=True)
        row.prop(md, "pass_index", text="Pass")
        row.prop(md, "invert_material_pass", text="", icon='ARROW_LEFTRIGHT')

        col.label(text="Layer:")
        row = col.row(align=True)
        row.prop_search(md, "layer", gpd, "layers", text="", icon='GREASEPENCIL')
        row.prop(md, "invert_layers", text="", icon='ARROW_LEFTRIGHT')
        row = layout.row(align=True)
        row.prop(md, "layer_pass", text="Pass")
        row.prop(md, "invert_layer_pass", text="", icon='ARROW_LEFTRIGHT')

    def GP_OPACITY(self, layout, ob, md):
        gpd = ob.data
        split = layout.split()

        col = split.column()
        col.label(text="Opacity:")
        col.prop(md, "factor")

        row = layout.row()
        row.prop(md, "create_materials")
        row.prop(md, "modify_color")

        col = layout.column()
        col.separator()
        col.label(text="Vertex Group:")
        row = col.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        row.prop(md, "invert_vertex", text="", icon='ARROW_LEFTRIGHT')

        col.label(text="Material:")
        row = col.row(align=True)
        row.prop(md, "pass_index", text="Pass")
        row.prop(md, "invert_material_pass", text="", icon='ARROW_LEFTRIGHT')

        col.label(text="Layer:")
        row = col.row(align=True)
        row.prop_search(md, "layer", gpd, "layers", text="", icon='GREASEPENCIL')
        row.prop(md, "invert_layers", text="", icon='ARROW_LEFTRIGHT')
        row = layout.row(align=True)
        row.prop(md, "layer_pass", text="Pass")
        row.prop(md, "invert_layer_pass", text="", icon='ARROW_LEFTRIGHT')

    def GP_ARRAY(self, layout, ob, md):
        gpd = ob.data

        col = layout.column()
        col.prop(md, "count")

        split = layout.split()
        col = split.column()
        col.label(text="Offset:")
        col.prop(md, "offset", text="")
        col.prop(md, "offset_object", text="Object")

        col = split.column()
        col.label(text="Shift:")
        col.prop(md, "shift", text="")

        split = layout.split()
        col = split.column()
        col.label(text="Rotation:")
        col.prop(md, "rotation", text="")
        col.separator()
        row = col.row(align=True)
        row.prop(md, "random_rot", text="", icon='TIME', toggle=True)
        row.prop(md, "rot_factor", text="")

        col = split.column()
        col.label(text="Scale:")
        col.prop(md, "scale", text="")
        col.separator()
        row = col.row(align=True)
        row.prop(md, "random_scale", text="", icon='TIME', toggle=True)
        row.prop(md, "scale_factor", text="")

        col = layout.column()
        col.prop(md, "replace_material", text="Material")
        col.prop(md, "keep_on_top", text="Keep original stroke on top")

        col = layout.column()
        col.separator()
        col.label(text="Material:")
        row = col.row(align=True)
        row.prop(md, "pass_index", text="Pass")
        row.prop(md, "invert_material_pass", text="", icon='ARROW_LEFTRIGHT')

        col.label(text="Layer:")
        row = col.row(align=True)
        row.prop_search(md, "layer", gpd, "layers", text="", icon='GREASEPENCIL')
        row.prop(md, "invert_layers", text="", icon='ARROW_LEFTRIGHT')
        row = layout.row(align=True)
        row.prop(md, "layer_pass", text="Pass")
        row.prop(md, "invert_layer_pass", text="", icon='ARROW_LEFTRIGHT')

    def GP_BUILD(self, layout, ob, md):
        gpd = ob.data

        split = layout.split()

        col = split.column()
#       self.check_conflicts(col, ob)

        col.prop(md, "mode")
        if md.mode == 'CONCURRENT':
            col.prop(md, "concurrent_time_alignment")

        col.separator()
        col.prop(md, "transition")
        sub = col.column(align=True)
        sub.prop(md, "start_delay")
        sub.prop(md, "length")

        col = layout.column(align=True)
        col.prop(md, "use_restrict_frame_range")
        sub = col.column(align=True)
        sub.active = md.use_restrict_frame_range
        sub.prop(md, "frame_start", text="Start")
        sub.prop(md, "frame_end", text="End")

        col = layout.column()
        col.separator()
        col.label(text="Layer:")
        row = col.row(align=True)
        row.prop_search(md, "layer", gpd, "layers", text="", icon='GREASEPENCIL')
        row.prop(md, "invert_layers", text="", icon='ARROW_LEFTRIGHT')
        row = layout.row(align=True)
        row.prop(md, "layer_pass", text="Pass")
        row.prop(md, "invert_layer_pass", text="", icon='ARROW_LEFTRIGHT')

    def GP_LATTICE(self, layout, ob, md):
        gpd = ob.data
        split = layout.split()

        col = split.column()
        col.label(text="Object:")
        col.prop(md, "object", text="")

        layout.prop(md, "strength", slider=True)

        col = layout.column()
        col.separator()
        col.label(text="Vertex Group:")
        row = col.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        row.prop(md, "invert_vertex", text="", icon='ARROW_LEFTRIGHT')

        col.label(text="Material:")
        row = col.row(align=True)
        row.prop(md, "pass_index", text="Pass")
        row.prop(md, "invert_material_pass", text="", icon='ARROW_LEFTRIGHT')

        col.label(text="Layer:")
        row = col.row(align=True)
        row.prop_search(md, "layer", gpd, "layers", text="", icon='GREASEPENCIL')
        row.prop(md, "invert_layers", text="", icon='ARROW_LEFTRIGHT')
        row = layout.row(align=True)
        row.prop(md, "layer_pass", text="Pass")
        row.prop(md, "invert_layer_pass", text="", icon='ARROW_LEFTRIGHT')

    def GP_MIRROR(self, layout, ob, md):
        gpd = ob.data

        row = layout.row(align=True)
        row.prop(md, "x_axis")
        row.prop(md, "y_axis")
        row.prop(md, "z_axis")

        layout.label(text="Object:")
        layout.prop(md, "object", text="")

        col = layout.column()
        col.separator()
        col.label(text="Material:")
        row = col.row(align=True)
        row.prop(md, "pass_index", text="Pass")
        row.prop(md, "invert_material_pass", text="", icon='ARROW_LEFTRIGHT')

        col.label(text="Layer:")
        row = col.row(align=True)
        row.prop_search(md, "layer", gpd, "layers", text="", icon='GREASEPENCIL')
        row.prop(md, "invert_layers", text="", icon='ARROW_LEFTRIGHT')
        row = layout.row(align=True)
        row.prop(md, "layer_pass", text="Pass")
        row.prop(md, "invert_layer_pass", text="", icon='ARROW_LEFTRIGHT')

    def GP_HOOK(self, layout, ob, md):
        gpd = ob.data
        split = layout.split()

        col = split.column()
        col.label(text="Object:")
        col.prop(md, "object", text="")
        if md.object and md.object.type == 'ARMATURE':
            col.label(text="Bone:")
            col.prop_search(md, "subtarget", md.object.data, "bones", text="")

        use_falloff = (md.falloff_type != 'NONE')

        layout.separator()

        row = layout.row(align=True)
        if use_falloff:
            row.prop(md, "falloff_radius")
        row.prop(md, "strength", slider=True)
        layout.prop(md, "falloff_type")

        col = layout.column()
        if use_falloff:
            if md.falloff_type == 'CURVE':
                col.template_curve_mapping(md, "falloff_curve")

        split = layout.split()

        col = split.column()
        col.prop(md, "use_falloff_uniform")

        col = layout.column()
        col.separator()
        col.label(text="Vertex Group:")
        row = col.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        row.prop(md, "invert_vertex", text="", icon='ARROW_LEFTRIGHT')

        col.label(text="Material:")
        row = col.row(align=True)
        row.prop(md, "pass_index", text="Pass")
        row.prop(md, "invert_material_pass", text="", icon='ARROW_LEFTRIGHT')

        col.label(text="Layer:")
        row = col.row(align=True)
        row.prop_search(md, "layer", gpd, "layers", text="", icon='GREASEPENCIL')
        row.prop(md, "invert_layers", text="", icon='ARROW_LEFTRIGHT')
        row = layout.row(align=True)
        row.prop(md, "layer_pass", text="Pass")
        row.prop(md, "invert_layer_pass", text="", icon='ARROW_LEFTRIGHT')

    def GP_OFFSET(self, layout, ob, md):
        gpd = ob.data
        col = layout.column()

        col.prop(md, "location")
        col.prop(md, "scale")
        col.prop(md, "rotation")

        col = layout.column()
        col.separator()
        col.label(text="Vertex Group:")
        row = col.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        row.prop(md, "invert_vertex", text="", icon='ARROW_LEFTRIGHT')

        col.label(text="Material:")
        row = col.row(align=True)
        row.prop(md, "pass_index", text="Pass")
        row.prop(md, "invert_material_pass", text="", icon='ARROW_LEFTRIGHT')

        col.label(text="Layer:")
        row = col.row(align=True)
        row.prop_search(md, "layer", gpd, "layers", text="", icon='GREASEPENCIL')
        row.prop(md, "invert_layers", text="", icon='ARROW_LEFTRIGHT')
        row = layout.row(align=True)
        row.prop(md, "layer_pass", text="Pass")
        row.prop(md, "invert_layer_pass", text="", icon='ARROW_LEFTRIGHT')

    def GP_ARMATURE(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Object:")
        col.prop(md, "object", text="")
        # col.prop(md, "use_deform_preserve_volume")

        col = split.column()
        col.label(text="Bind To:")
        col.prop(md, "use_vertex_groups", text="Vertex Groups")
        col.prop(md, "use_bone_envelopes", text="Bone Envelopes")

        layout.separator()

        row = layout.row(align=True)
        row.label(text="Vertex Group:")
        row = layout.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        sub = row.row(align=True)
        sub.active = bool(md.vertex_group)
        sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')




    def ARMATURE(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Object:")
        col.prop(md, "object", text="")
        col.prop(md, "use_deform_preserve_volume")

        col = split.column()
        col.label(text="Bind To:")
        col.prop(md, "use_vertex_groups", text="Vertex Groups")
        col.prop(md, "use_bone_envelopes", text="Bone Envelopes")

        layout.separator()

        split = layout.split()

        row = split.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        sub = row.row(align=True)
        sub.active = bool(md.vertex_group)
        sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

        split.prop(md, "use_multi_modifier")

    def ARRAY(self, layout, ob, md):
        layout.prop(md, "fit_type")

        if md.fit_type == 'FIXED_COUNT':
            layout.prop(md, "count")
        elif md.fit_type == 'FIT_LENGTH':
            layout.prop(md, "fit_length")
        elif md.fit_type == 'FIT_CURVE':
            layout.prop(md, "curve")

        layout.separator()

        split = layout.split()

        col = split.column()
        col.prop(md, "use_constant_offset")
        sub = col.column()
        sub.active = md.use_constant_offset
        sub.prop(md, "constant_offset_displace", text="")

        col.separator()

        col.prop(md, "use_merge_vertices", text="Merge")
        sub = col.column()
        sub.active = md.use_merge_vertices
        sub.prop(md, "use_merge_vertices_cap", text="First Last")
        sub.prop(md, "merge_threshold", text="Distance")

        col = split.column()
        col.prop(md, "use_relative_offset")
        sub = col.column()
        sub.active = md.use_relative_offset
        sub.prop(md, "relative_offset_displace", text="")

        col.separator()

        col.prop(md, "use_object_offset")
        sub = col.column()
        sub.active = md.use_object_offset
        sub.prop(md, "offset_object", text="")

        row = layout.row()
        split = row.split()
        col = split.column()
        col.label(text="UVs:")
        sub = col.column(align=True)
        sub.prop(md, "offset_u")
        sub.prop(md, "offset_v")
        layout.separator()

        layout.prop(md, "start_cap")
        layout.prop(md, "end_cap")

    def BEVEL(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.prop(md, "width")
        col.prop(md, "segments")
        col.prop(md, "profile")
        col.prop(md, "material")

        col = split.column()
        col.prop(md, "use_only_vertices")
        col.prop(md, "use_clamp_overlap")
        col.prop(md, "loop_slide")
        col.prop(md, "mark_seam")
        col.prop(md, "mark_sharp")

        layout.label(text="Limit Method:")
        layout.row().prop(md, "limit_method", expand=True)
        if md.limit_method == 'ANGLE':
            layout.prop(md, "angle_limit")
        elif md.limit_method == 'VGROUP':
            layout.label(text="Vertex Group:")
            layout.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

        layout.label(text="Width Method:")
        layout.row().prop(md, "offset_type", expand=True)

        layout.label(text="Normal Mode")
        layout.row().prop(md, "hnmode", expand=True)
        layout.prop(md, "hn_strength")
        layout.prop(md, "set_wn_strength")

    def BOOLEAN(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Operation:")
        col.prop(md, "operation", text="")

        col = split.column()
        col.label(text="Object:")
        col.prop(md, "object", text="")

        layout.prop(md, "double_threshold")

        if bpy.app.debug:
            layout.prop(md, "debug_options")

    def BUILD(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.prop(md, "frame_start")
        col.prop(md, "frame_duration")
        col.prop(md, "use_reverse")

        col = split.column()
        col.prop(md, "use_random_order")
        sub = col.column()
        sub.active = md.use_random_order
        sub.prop(md, "seed")

    def MESH_CACHE(self, layout, ob, md):
        layout.prop(md, "cache_format")
        layout.prop(md, "filepath")

        if md.cache_format == 'ABC':
            layout.prop(md, "sub_object")

        layout.label(text="Evaluation:")
        layout.prop(md, "factor", slider=True)
        layout.prop(md, "deform_mode")
        layout.prop(md, "interpolation")

        layout.label(text="Time Mapping:")

        row = layout.row()
        row.prop(md, "time_mode", expand=True)
        row = layout.row()
        row.prop(md, "play_mode", expand=True)
        if md.play_mode == 'SCENE':
            layout.prop(md, "frame_start")
            layout.prop(md, "frame_scale")
        else:
            time_mode = md.time_mode
            if time_mode == 'FRAME':
                layout.prop(md, "eval_frame")
            elif time_mode == 'TIME':
                layout.prop(md, "eval_time")
            elif time_mode == 'FACTOR':
                layout.prop(md, "eval_factor")

        layout.label(text="Axis Mapping:")
        split = layout.split(factor=0.5, align=True)
        split.alert = (md.forward_axis[-1] == md.up_axis[-1])
        split.label(text="Forward/Up Axis:")
        split.prop(md, "forward_axis", text="")
        split.prop(md, "up_axis", text="")
        split = layout.split(factor=0.5)
        split.label(text="Flip Axis:")
        row = split.row()
        row.prop(md, "flip_axis")

    def MESH_SEQUENCE_CACHE(self, layout, ob, md):
        layout.label(text="Cache File Properties:")
        box = layout.box()
        box.template_cache_file(md, "cache_file")

        cache_file = md.cache_file

        layout.label(text="Modifier Properties:")
        box = layout.box()

        if cache_file is not None:
            box.prop_search(md, "object_path", cache_file, "object_paths")

        if ob.type == 'MESH':
            box.row().prop(md, "read_data")

    def CAST(self, layout, ob, md):
        split = layout.split(factor=0.25)

        split.label(text="Cast Type:")
        split.prop(md, "cast_type", text="")

        split = layout.split(factor=0.25)

        col = split.column()
        col.prop(md, "use_x")
        col.prop(md, "use_y")
        col.prop(md, "use_z")

        col = split.column()
        col.prop(md, "factor")
        col.prop(md, "radius")
        col.prop(md, "size")
        col.prop(md, "use_radius_as_size")

        split = layout.split()

        col = split.column()
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        col = split.column()
        col.label(text="Control Object:")
        col.prop(md, "object", text="")
        if md.object:
            col.prop(md, "use_transform")

    def CLOTH(self, layout, ob, md):
        layout.label(text="Settings are inside the Physics tab")

    def COLLISION(self, layout, ob, md):
        layout.label(text="Settings are inside the Physics tab")

    def CURVE(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Object:")
        col.prop(md, "object", text="")
        col = split.column()
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        layout.label(text="Deformation Axis:")
        layout.row().prop(md, "deform_axis", expand=True)

    def DECIMATE(self, layout, ob, md):
        decimate_type = md.decimate_type

        row = layout.row()
        row.prop(md, "decimate_type", expand=True)

        if decimate_type == 'COLLAPSE':
            has_vgroup = bool(md.vertex_group)
            layout.prop(md, "ratio")

            split = layout.split()

            col = split.column()
            row = col.row(align=True)
            row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
            row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

            layout_info = col

            col = split.column()
            row = col.row()
            row.active = has_vgroup
            row.prop(md, "vertex_group_factor")

            col.prop(md, "use_collapse_triangulate")
            row = col.split(factor=0.75)
            row.prop(md, "use_symmetry")
            row.prop(md, "symmetry_axis", text="")

        elif decimate_type == 'UNSUBDIV':
            layout.prop(md, "iterations")
            layout_info = layout
        else:  # decimate_type == 'DISSOLVE':
            layout.prop(md, "angle_limit")
            layout.prop(md, "use_dissolve_boundaries")
            layout.label(text="Delimit:")
            row = layout.row()
            row.prop(md, "delimit")
            layout_info = layout

        layout_info.label(
            text=iface_("Face Count: {:,}".format(md.face_count)),
            translate=False,
        )

    def DISPLACE(self, layout, ob, md):
        has_texture = (md.texture is not None)

        col = layout.column(align=True)
        col.label(text="Texture:")
        col.template_ID(md, "texture", new="texture.new")

        split = layout.split()

        col = split.column(align=True)
        col.label(text="Direction:")
        col.prop(md, "direction", text="")
        if md.direction in {'X', 'Y', 'Z', 'RGB_TO_XYZ'}:
            col.label(text="Space:")
            col.prop(md, "space", text="")
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

        col = split.column(align=True)
        col.active = has_texture
        col.label(text="Texture Coordinates:")
        col.prop(md, "texture_coords", text="")
        if md.texture_coords == 'OBJECT':
            col.label(text="Object:")
            col.prop(md, "texture_coords_object", text="")
        elif md.texture_coords == 'UV' and ob.type == 'MESH':
            col.label(text="UV Map:")
            col.prop_search(md, "uv_layer", ob.data, "uv_layers", text="")

        layout.separator()

        row = layout.row()
        row.prop(md, "mid_level")
        row.prop(md, "strength")

    def DYNAMIC_PAINT(self, layout, ob, md):
        layout.label(text="Settings are inside the Physics tab")

    def EDGE_SPLIT(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.prop(md, "use_edge_angle", text="Edge Angle")
        sub = col.column()
        sub.active = md.use_edge_angle
        sub.prop(md, "split_angle")

        split.prop(md, "use_edge_sharp", text="Sharp Edges")

    def EXPLODE(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        sub = col.column()
        sub.active = bool(md.vertex_group)
        sub.prop(md, "protect")
        col.label(text="Particle UV")
        col.prop_search(md, "particle_uv", ob.data, "uv_layers", text="")

        col = split.column()
        col.prop(md, "use_edge_cut")
        col.prop(md, "show_unborn")
        col.prop(md, "show_alive")
        col.prop(md, "show_dead")
        col.prop(md, "use_size")

        layout.operator("object.explode_refresh", text="Refresh")

    def FLUID_SIMULATION(self, layout, ob, md):
        layout.label(text="Settings are inside the Physics tab")

    def HOOK(self, layout, ob, md):
        use_falloff = (md.falloff_type != 'NONE')
        split = layout.split()

        col = split.column()
        col.label(text="Object:")
        col.prop(md, "object", text="")
        if md.object and md.object.type == 'ARMATURE':
            col.label(text="Bone:")
            col.prop_search(md, "subtarget", md.object.data, "bones", text="")
        col = split.column()
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

        layout.separator()

        row = layout.row(align=True)
        if use_falloff:
            row.prop(md, "falloff_radius")
        row.prop(md, "strength", slider=True)
        layout.prop(md, "falloff_type")

        col = layout.column()
        if use_falloff:
            if md.falloff_type == 'CURVE':
                col.template_curve_mapping(md, "falloff_curve")

        split = layout.split()

        col = split.column()
        col.prop(md, "use_falloff_uniform")

        if ob.mode == 'EDIT':
            row = col.row(align=True)
            row.operator("object.hook_reset", text="Reset")
            row.operator("object.hook_recenter", text="Recenter")

            row = layout.row(align=True)
            row.operator("object.hook_select", text="Select")
            row.operator("object.hook_assign", text="Assign")

    def LAPLACIANDEFORM(self, layout, ob, md):
        is_bind = md.is_bind

        layout.prop(md, "iterations")

        row = layout.row()
        row.active = not is_bind
        row.label(text="Anchors Vertex Group:")

        row = layout.row()
        row.enabled = not is_bind
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

        layout.separator()

        row = layout.row()
        row.enabled = bool(md.vertex_group)
        row.operator("object.laplaciandeform_bind", text="Unbind" if is_bind else "Bind")

    def LAPLACIANSMOOTH(self, layout, ob, md):
        layout.prop(md, "iterations")

        split = layout.split(factor=0.25)

        col = split.column()
        col.label(text="Axis:")
        col.prop(md, "use_x")
        col.prop(md, "use_y")
        col.prop(md, "use_z")

        col = split.column()
        col.label(text="Lambda:")
        col.prop(md, "lambda_factor", text="Factor")
        col.prop(md, "lambda_border", text="Border")

        col.separator()
        col.prop(md, "use_volume_preserve")
        col.prop(md, "use_normalized")

        layout.label(text="Vertex Group:")
        layout.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

    def LATTICE(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Object:")
        col.prop(md, "object", text="")

        col = split.column()
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

        layout.separator()
        layout.prop(md, "strength", slider=True)

    def MASK(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Mode:")
        col.prop(md, "mode", text="")

        col = split.column()
        if md.mode == 'ARMATURE':
            col.label(text="Armature:")
            row = col.row(align=True)
            row.prop(md, "armature", text="")
            sub = row.row(align=True)
            sub.active = (md.armature is not None)
            sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
        elif md.mode == 'VERTEX_GROUP':
            col.label(text="Vertex Group:")
            row = col.row(align=True)
            row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
            sub = row.row(align=True)
            sub.active = bool(md.vertex_group)
            sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

    def MESH_DEFORM(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.enabled = not md.is_bound
        col.label(text="Object:")
        col.prop(md, "object", text="")

        col = split.column()
        col.label(text="Vertex Group:")
        row = col.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        sub = row.row(align=True)
        sub.active = bool(md.vertex_group)
        sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

        layout.separator()
        row = layout.row()
        row.enabled = not md.is_bound
        row.prop(md, "precision")
        row.prop(md, "use_dynamic_bind")

        layout.separator()
        if md.is_bound:
            layout.operator("object.meshdeform_bind", text="Unbind")
        else:
            layout.operator("object.meshdeform_bind", text="Bind")

    def MIRROR(self, layout, ob, md):
        axis_text = "XYZ"
        split = layout.split(factor=0.33)

        col = split.column()
        col.label(text="Axis:")
        for i, text in enumerate(axis_text):
            col.prop(md, "use_axis", text=text, index=i)

        col = split.column()
        col.label(text="Bisect:")
        for i, text in enumerate(axis_text):
            colsub = col.column()
            colsub.prop(md, "use_bisect_axis", text=text, index=i)
            colsub.active = md.use_axis[i]

        col = split.column()
        col.label(text="Flip:")
        for i, text in enumerate(axis_text):
            colsub = col.column()
            colsub.prop(md, "use_bisect_flip_axis", text=text, index=i)
            colsub.active = md.use_axis[i] and md.use_bisect_axis[i]

        col = layout.column()
        col.label(text="Mirror Object:")
        col.prop(md, "mirror_object", text="")

        # col = layout.column()

        # row = layout.row()
        # row.prop(md, "use_mirror_vertex_groups", text="Vertex Groups")
        # row.prop(md, "use_clip", text="Clipping")
        # row = layout.row()
        # row.prop(md, "use_mirror_merge", text="Merge")

        # col = layout.column()
        # if md.use_mirror_merge is True:
            # col.prop(md, "merge_threshold")

        # col = layout.column()


        # flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        # col.label(text="Textures:")
        # row = layout.row()
        # row.prop(md, "use_mirror_u", text="Flip U")
        # row.prop(md, "use_mirror_v", text="Flip V")

        # col = layout.column(align=True)

        # if md.use_mirror_u:
            # col.prop(md, "mirror_offset_u")

        # if md.use_mirror_v:
            # col.prop(md, "mirror_offset_v")

        # col = layout.column(align=True)
        # col.prop(md, "offset_u")
        # col.prop(md, "offset_v")


    def MULTIRES(self, layout, ob, md):
        layout.row().prop(md, "subdivision_type", expand=True)

        split = layout.split()
        col = split.column()
        col.prop(md, "levels", text="Preview")
        col.prop(md, "sculpt_levels", text="Sculpt")
        col.prop(md, "render_levels", text="Render")
        if hasattr(md, "quality"):
            col.prop(md, "quality")

        col = split.column()

        col.enabled = ob.mode != 'EDIT'
        col.operator("object.multires_subdivide", text="Subdivide")
        col.operator("object.multires_higher_levels_delete", text="Delete Higher")
        col.operator("object.multires_reshape", text="Reshape")
        col.operator("object.multires_base_apply", text="Apply Base")
        col.prop(md, "uv_smooth", text="")
        col.prop(md, "show_only_control_edges")

        layout.separator()

        col = layout.column()
        row = col.row()
        if md.is_external:
            row.operator("object.multires_external_pack", text="Pack External")
            row.label()
            row = col.row()
            row.prop(md, "filepath", text="")
        else:
            row.operator("object.multires_external_save", text="Save External...")
            row.label()

    def OCEAN(self, layout, ob, md):
        if not bpy.app.build_options.mod_oceansim:
            layout.label(text="Built without OceanSim modifier")
            return

        layout.prop(md, "geometry_mode")

        if md.geometry_mode == 'GENERATE':
            row = layout.row()
            row.prop(md, "repeat_x")
            row.prop(md, "repeat_y")

        layout.separator()

        split = layout.split()

        col = split.column()
        col.prop(md, "time")
        col.prop(md, "depth")
        col.prop(md, "random_seed")

        col = split.column()
        col.prop(md, "resolution")
        col.prop(md, "size")
        col.prop(md, "spatial_size")

        layout.label(text="Waves:")

        split = layout.split()

        col = split.column()
        col.prop(md, "choppiness")
        col.prop(md, "wave_scale", text="Scale")
        col.prop(md, "wave_scale_min")
        col.prop(md, "wind_velocity")

        col = split.column()
        col.prop(md, "wave_alignment", text="Alignment")
        sub = col.column()
        sub.active = (md.wave_alignment > 0.0)
        sub.prop(md, "wave_direction", text="Direction")
        sub.prop(md, "damping")

        layout.separator()

        layout.prop(md, "use_normals")

        split = layout.split()

        col = split.column()
        col.prop(md, "use_foam")
        sub = col.row()
        sub.active = md.use_foam
        sub.prop(md, "foam_coverage", text="Coverage")

        col = split.column()
        col.active = md.use_foam
        col.label(text="Foam Data Layer Name:")
        col.prop(md, "foam_layer_name", text="")

        layout.separator()

        if md.is_cached:
            layout.operator("object.ocean_bake", text="Free Bake").free = True
        else:
            layout.operator("object.ocean_bake").free = False

        split = layout.split()
        split.enabled = not md.is_cached

        col = split.column(align=True)
        col.prop(md, "frame_start", text="Start")
        col.prop(md, "frame_end", text="End")

        col = split.column(align=True)
        col.label(text="Cache path:")
        col.prop(md, "filepath", text="")

        split = layout.split()
        split.enabled = not md.is_cached

        col = split.column()
        col.active = md.use_foam
        col.prop(md, "bake_foam_fade")

        col = split.column()

    def PARTICLE_INSTANCE(self, layout, ob, md):
        layout.prop(md, "object")
        if md.object:
            layout.prop_search(md, "particle_system", md.object, "particle_systems", text="Particle System")
        else:
            layout.prop(md, "particle_system_index", text="Particle System")

        split = layout.split()
        col = split.column()
        col.label(text="Create From:")
        layout.prop(md, "space", text="")
        col.prop(md, "use_normal")
        col.prop(md, "use_children")
        col.prop(md, "use_size")

        col = split.column()
        col.label(text="Show Particles When:")
        col.prop(md, "show_alive")
        col.prop(md, "show_unborn")
        col.prop(md, "show_dead")

        row = layout.row(align=True)
        row.prop(md, "particle_amount", text="Amount")
        row.prop(md, "particle_offset", text="Offset")

        row = layout.row(align=True)
        row.prop(md, "axis", expand=True)

        layout.separator()

        layout.prop(md, "use_path", text="Create Along Paths")

        col = layout.column()
        col.active = md.use_path
        col.prop(md, "use_preserve_shape")

        row = col.row(align=True)
        row.prop(md, "position", slider=True)
        row.prop(md, "random_position", text="Random", slider=True)
        row = col.row(align=True)
        row.prop(md, "rotation", slider=True)
        row.prop(md, "random_rotation", text="Random", slider=True)

        layout.separator()

        col = layout.column()
        col.prop_search(md, "index_layer_name", ob.data, "vertex_colors", text="Index Layer")
        col.prop_search(md, "value_layer_name", ob.data, "vertex_colors", text="Value Layer")

    def PARTICLE_SYSTEM(self, layout, ob, md):
        layout.label(text="Settings can be found inside the Particle context")

    def SCREW(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.prop(md, "axis")
        col.prop(md, "object", text="AxisOb")
        col.prop(md, "angle")
        col.prop(md, "steps")
        col.prop(md, "render_steps")
        col.prop(md, "use_smooth_shade")
        col.prop(md, "use_merge_vertices")
        sub = col.column()
        sub.active = md.use_merge_vertices
        sub.prop(md, "merge_threshold")

        col = split.column()
        row = col.row()
        row.active = (md.object is None or md.use_object_screw_offset is False)
        row.prop(md, "screw_offset")
        row = col.row()
        row.active = (md.object is not None)
        row.prop(md, "use_object_screw_offset")
        col.prop(md, "use_normal_calculate")
        col.prop(md, "use_normal_flip")
        col.prop(md, "iterations")
        col.prop(md, "use_stretch_u")
        col.prop(md, "use_stretch_v")

    def SHRINKWRAP(self, layout, ob, md):
        split = layout.split()
        col = split.column()
        col.label(text="Target:")
        col.prop(md, "target", text="")
        col = split.column()
        col.label(text="Vertex Group:")
        row = col.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

        split = layout.split()

        col = split.column()
        col.prop(md, "offset")

        col = split.column()
        col.label(text="Mode:")
        col.prop(md, "wrap_method", text="")

        if md.wrap_method in {'PROJECT', 'NEAREST_SURFACEPOINT'}:
            col.prop(md, "wrap_mode", text="")

        if md.wrap_method == 'PROJECT':
            split = layout.split()
            col = split.column()
            col.prop(md, "subsurf_levels")
            col = split.column()

            col.prop(md, "project_limit", text="Limit")
            split = layout.split(factor=0.25)

            col = split.column()
            col.label(text="Axis:")
            col.prop(md, "use_project_x")
            col.prop(md, "use_project_y")
            col.prop(md, "use_project_z")

            col = split.column()
            col.label(text="Direction:")
            col.prop(md, "use_negative_direction")
            col.prop(md, "use_positive_direction")

            subcol = col.column()
            subcol.active = md.use_negative_direction and md.cull_face != 'OFF'
            subcol.prop(md, "use_invert_cull")

            col = split.column()
            col.label(text="Cull Faces:")
            col.prop(md, "cull_face", expand=True)

            layout.prop(md, "auxiliary_target")

    def SIMPLE_DEFORM(self, layout, ob, md):

        layout.row().prop(md, "deform_method", expand=True)

        split = layout.split()

        col = split.column()
        col.label(text="Vertex Group:")
        row = col.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

        split = layout.split()

        col = split.column()
        col.label(text="Axis, Origin:")
        col.prop(md, "origin", text="")

        col.prop(md, "deform_axis")

        if md.deform_method in {'TAPER', 'STRETCH', 'TWIST'}:
            row = col.row(align=True)
            row.label(text="Lock:")
            deform_axis = md.deform_axis
            if deform_axis != 'X':
                row.prop(md, "lock_x")
            if deform_axis != 'Y':
                row.prop(md, "lock_y")
            if deform_axis != 'Z':
                row.prop(md, "lock_z")

        col = split.column()
        col.label(text="Deform:")
        if md.deform_method in {'TAPER', 'STRETCH'}:
            col.prop(md, "factor")
        else:
            col.prop(md, "angle")
        col.prop(md, "limits", slider=True)

    def SMOKE(self, layout, ob, md):
        layout.label(text="Settings are inside the Physics tab")

    def SMOOTH(self, layout, ob, md):
        split = layout.split(factor=0.25)

        col = split.column()
        col.label(text="Axis:")
        col.prop(md, "use_x")
        col.prop(md, "use_y")
        col.prop(md, "use_z")

        col = split.column()
        col.prop(md, "factor")
        col.prop(md, "iterations")
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

    def SOFT_BODY(self, layout, ob, md):
        layout.label(text="Settings are inside the Physics tab")

    def SOLIDIFY(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.prop(md, "thickness")
        col.prop(md, "thickness_clamp")

        col.separator()

        row = col.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        sub = row.row(align=True)
        sub.active = bool(md.vertex_group)
        sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

        sub = col.row()
        sub.active = bool(md.vertex_group)
        sub.prop(md, "thickness_vertex_group", text="Factor")

        col.label(text="Crease:")
        col.prop(md, "edge_crease_inner", text="Inner")
        col.prop(md, "edge_crease_outer", text="Outer")
        col.prop(md, "edge_crease_rim", text="Rim")

        col = split.column()

        col.prop(md, "offset")
        col.prop(md, "use_flip_normals")

        col.prop(md, "use_even_offset")
        col.prop(md, "use_quality_normals")
        col.prop(md, "use_rim")
        col_rim = col.column()
        col_rim.active = md.use_rim
        col_rim.prop(md, "use_rim_only")

        col.separator()

        col.label(text="Material Index Offset:")

        sub = col.column()
        row = sub.split(factor=0.4, align=True)
        row.prop(md, "material_offset", text="")
        row = row.row(align=True)
        row.active = md.use_rim
        row.prop(md, "material_offset_rim", text="Rim")

    def SUBSURF(self, layout, ob, md):
        from bpy import context
        layout.row().prop(md, "subdivision_type", expand=True)

        split = layout.split()
        col = split.column()

        scene = context.scene
        engine = context.engine
        show_adaptive_options = (
            engine == 'CYCLES' and md == ob.modifiers[-1] and
            scene.cycles.feature_set == 'EXPERIMENTAL'
        )
        if show_adaptive_options:
            col.label(text="View:")
            col.prop(md, "levels", text="Levels")
            col.label(text="Render:")
            col.prop(ob.cycles, "use_adaptive_subdivision", text="Adaptive")
            if ob.cycles.use_adaptive_subdivision:
                col.prop(ob.cycles, "dicing_rate")
            else:
                col.prop(md, "render_levels", text="Levels")
        else:
            col.label(text="Subdivisions:")
            col.prop(md, "levels", text="View")
            col.prop(md, "render_levels", text="Render")
            if hasattr(md, "quality"):
                col.prop(md, "quality")

        col = split.column()
        col.label(text="Options:")

        sub = col.column()
        sub.active = (not show_adaptive_options) or (not ob.cycles.use_adaptive_subdivision)
        sub.prop(md, "uv_smooth", text="")

        col.prop(md, "show_only_control_edges")

        if show_adaptive_options and ob.cycles.use_adaptive_subdivision:
            col = layout.column(align=True)
            col.scale_y = 0.6
            col.separator()
            col.label(text="Final Dicing Rate:")
            col.separator()

            render = max(scene.cycles.dicing_rate * ob.cycles.dicing_rate, 0.1)
            preview = max(scene.cycles.preview_dicing_rate * ob.cycles.dicing_rate, 0.1)
            col.label(text=f"Render {render:.2f} px, Preview {preview:.2f} px")

    def SURFACE(self, layout, ob, md):
        layout.label(text="Settings are inside the Physics tab")

    def SURFACE_DEFORM(self, layout, ob, md):
        col = layout.column()
        col.active = not md.is_bound

        col.prop(md, "target")
        col.prop(md, "falloff")

        layout.separator()

        col = layout.column()

        if md.is_bound:
            col.operator("object.surfacedeform_bind", text="Unbind")
        else:
            col.active = md.target is not None
            col.operator("object.surfacedeform_bind", text="Bind")

    def UV_PROJECT(self, layout, ob, md):
        split = layout.split()
        col = split.column()
        col.prop_search(md, "uv_layer", ob.data, "uv_layers")
        col.separator()

        col.prop(md, "projector_count", text="Projectors")
        for proj in md.projectors:
            col.prop(proj, "object", text="")

        col = split.column()
        sub = col.column(align=True)
        sub.prop(md, "aspect_x", text="Aspect X")
        sub.prop(md, "aspect_y", text="Aspect Y")

        sub = col.column(align=True)
        sub.prop(md, "scale_x", text="Scale X")
        sub.prop(md, "scale_y", text="Scale Y")

    def WARP(self, layout, ob, md):
        use_falloff = (md.falloff_type != 'NONE')
        split = layout.split()

        col = split.column()
        col.label(text="From:")
        col.prop(md, "object_from", text="")

        col.prop(md, "use_volume_preserve")

        col = split.column()
        col.label(text="To:")
        col.prop(md, "object_to", text="")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

        col = layout.column()

        row = col.row(align=True)
        row.prop(md, "strength")
        if use_falloff:
            row.prop(md, "falloff_radius")

        col.prop(md, "falloff_type")
        if use_falloff:
            if md.falloff_type == 'CURVE':
                col.template_curve_mapping(md, "falloff_curve")

        # 2 new columns
        split = layout.split()
        col = split.column()
        col.label(text="Texture:")
        col.template_ID(md, "texture", new="texture.new")

        col = split.column()
        col.label(text="Texture Coordinates:")
        col.prop(md, "texture_coords", text="")

        if md.texture_coords == 'OBJECT':
            layout.prop(md, "texture_coords_object", text="Object")
        elif md.texture_coords == 'UV' and ob.type == 'MESH':
            layout.prop_search(md, "uv_layer", ob.data, "uv_layers")

    def WAVE(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Motion:")
        col.prop(md, "use_x")
        col.prop(md, "use_y")
        col.prop(md, "use_cyclic")

        col = split.column()
        col.prop(md, "use_normal")
        sub = col.column()
        sub.active = md.use_normal
        sub.prop(md, "use_normal_x", text="X")
        sub.prop(md, "use_normal_y", text="Y")
        sub.prop(md, "use_normal_z", text="Z")

        split = layout.split()

        col = split.column()
        col.label(text="Time:")
        sub = col.column(align=True)
        sub.prop(md, "time_offset", text="Offset")
        sub.prop(md, "lifetime", text="Life")
        col.prop(md, "damping_time", text="Damping")

        col = split.column()
        col.label(text="Position:")
        sub = col.column(align=True)
        sub.prop(md, "start_position_x", text="X")
        sub.prop(md, "start_position_y", text="Y")
        col.prop(md, "falloff_radius", text="Falloff")

        layout.separator()

        layout.prop(md, "start_position_object")
        layout.prop_search(md, "vertex_group", ob, "vertex_groups")
        split = layout.split(factor=0.33)
        col = split.column()
        col.label(text="Texture")
        col = split.column()
        col.template_ID(md, "texture", new="texture.new")
        layout.prop(md, "texture_coords")
        if md.texture_coords == 'UV' and ob.type == 'MESH':
            layout.prop_search(md, "uv_layer", ob.data, "uv_layers")
        elif md.texture_coords == 'OBJECT':
            layout.prop(md, "texture_coords_object")

        layout.separator()

        split = layout.split()

        col = split.column()
        col.prop(md, "speed", slider=True)
        col.prop(md, "height", slider=True)

        col = split.column()
        col.prop(md, "width", slider=True)
        col.prop(md, "narrowness", slider=True)

    def REMESH(self, layout, ob, md):
        if not bpy.app.build_options.mod_remesh:
            layout.label(text="Built without Remesh modifier")
            return

        layout.prop(md, "mode")

        row = layout.row()
        row.prop(md, "octree_depth")
        row.prop(md, "scale")

        if md.mode == 'SHARP':
            layout.prop(md, "sharpness")

        layout.prop(md, "use_smooth_shade")
        layout.prop(md, "use_remove_disconnected")
        row = layout.row()
        row.active = md.use_remove_disconnected
        row.prop(md, "threshold")

    @staticmethod
    def vertex_weight_mask(layout, ob, md):
        layout.label(text="Influence/Mask Options:")

        split = layout.split(factor=0.4)
        split.label(text="Global Influence:")
        split.prop(md, "mask_constant", text="")

        if not md.mask_texture:
            split = layout.split(factor=0.4)
            split.label(text="Vertex Group Mask:")
            split.prop_search(md, "mask_vertex_group", ob, "vertex_groups", text="")

        if not md.mask_vertex_group:
            split = layout.split(factor=0.4)
            split.label(text="Texture Mask:")
            split.template_ID(md, "mask_texture", new="texture.new")
            if md.mask_texture:
                split = layout.split()

                col = split.column()
                col.label(text="Texture Coordinates:")
                col.prop(md, "mask_tex_mapping", text="")

                col = split.column()
                col.label(text="Use Channel:")
                col.prop(md, "mask_tex_use_channel", text="")

                if md.mask_tex_mapping == 'OBJECT':
                    layout.prop(md, "mask_tex_map_object", text="Object")
                elif md.mask_tex_mapping == 'UV' and ob.type == 'MESH':
                    layout.prop_search(md, "mask_tex_uv_layer", ob.data, "uv_layers")

    def VERTEX_WEIGHT_EDIT(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

        col.label(text="Default Weight:")
        col.prop(md, "default_weight", text="")

        col = split.column()
        col.prop(md, "use_add")
        sub = col.column()
        sub.active = md.use_add
        sub.prop(md, "add_threshold")

        col = col.column()
        col.prop(md, "use_remove")
        sub = col.column()
        sub.active = md.use_remove
        sub.prop(md, "remove_threshold")

        layout.separator()

        layout.prop(md, "falloff_type")
        if md.falloff_type == 'CURVE':
            layout.template_curve_mapping(md, "map_curve")

        # Common mask options
        layout.separator()
        self.vertex_weight_mask(layout, ob, md)

    def VERTEX_WEIGHT_MIX(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Vertex Group A:")
        col.prop_search(md, "vertex_group_a", ob, "vertex_groups", text="")
        col.label(text="Default Weight A:")
        col.prop(md, "default_weight_a", text="")

        col.label(text="Mix Mode:")
        col.prop(md, "mix_mode", text="")

        col = split.column()
        col.label(text="Vertex Group B:")
        col.prop_search(md, "vertex_group_b", ob, "vertex_groups", text="")
        col.label(text="Default Weight B:")
        col.prop(md, "default_weight_b", text="")

        col.label(text="Mix Set:")
        col.prop(md, "mix_set", text="")

        # Common mask options
        layout.separator()
        self.vertex_weight_mask(layout, ob, md)

    def VERTEX_WEIGHT_PROXIMITY(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

        col = split.column()
        col.label(text="Target Object:")
        col.prop(md, "target", text="")

        split = layout.split()

        col = split.column()
        col.label(text="Distance:")
        col.prop(md, "proximity_mode", text="")
        if md.proximity_mode == 'GEOMETRY':
            col.row().prop(md, "proximity_geometry")

        col = split.column()
        col.label()
        col.prop(md, "min_dist")
        col.prop(md, "max_dist")

        layout.separator()
        layout.prop(md, "falloff_type")

        # Common mask options
        layout.separator()
        self.vertex_weight_mask(layout, ob, md)

    def SKIN(self, layout, ob, md):
        row = layout.row()
        row.operator("object.skin_armature_create", text="Create Armature")
        row.operator("mesh.customdata_skin_add")

        layout.separator()

        row = layout.row(align=True)
        row.prop(md, "branch_smoothing")
        row.prop(md, "use_smooth_shade")

        split = layout.split()

        col = split.column()
        col.label(text="Selected Vertices:")
        sub = col.column(align=True)
        sub.operator("object.skin_loose_mark_clear", text="Mark Loose").action = 'MARK'
        sub.operator("object.skin_loose_mark_clear", text="Clear Loose").action = 'CLEAR'

        sub = col.column()
        sub.operator("object.skin_root_mark", text="Mark Root")
        sub.operator("object.skin_radii_equalize", text="Equalize Radii")

        col = split.column()
        col.label(text="Symmetry Axes:")
        col.prop(md, "use_x_symmetry")
        col.prop(md, "use_y_symmetry")
        col.prop(md, "use_z_symmetry")

    def TRIANGULATE(self, layout, ob, md):
        row = layout.row()

        col = row.column()
        col.label(text="Quad Method:")
        col.prop(md, "quad_method", text="")
        col = row.column()
        col.label(text="Ngon Method:")
        col.prop(md, "ngon_method", text="")

    def UV_WARP(self, layout, ob, md):
        split = layout.split()
        col = split.column()
        col.prop(md, "center")

        col = split.column()
        col.label(text="UV Axis:")
        col.prop(md, "axis_u", text="")
        col.prop(md, "axis_v", text="")

        split = layout.split()
        col = split.column()
        col.label(text="From:")
        col.prop(md, "object_from", text="")

        col = split.column()
        col.label(text="To:")
        col.prop(md, "object_to", text="")

        split = layout.split()
        col = split.column()
        obj = md.object_from
        if obj and obj.type == 'ARMATURE':
            col.label(text="Bone:")
            col.prop_search(md, "bone_from", obj.data, "bones", text="")

        col = split.column()
        obj = md.object_to
        if obj and obj.type == 'ARMATURE':
            col.label(text="Bone:")
            col.prop_search(md, "bone_to", obj.data, "bones", text="")

        split = layout.split()

        col = split.column()
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

        col = split.column()
        col.label(text="UV Map:")
        col.prop_search(md, "uv_layer", ob.data, "uv_layers", text="")

    def WIREFRAME(self, layout, ob, md):
        has_vgroup = bool(md.vertex_group)

        split = layout.split()

        col = split.column()
        col.prop(md, "thickness", text="Thickness")

        row = col.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        sub = row.row(align=True)
        sub.active = has_vgroup
        sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
        row = col.row(align=True)
        row.active = has_vgroup
        row.prop(md, "thickness_vertex_group", text="Factor")

        col.prop(md, "use_crease", text="Crease Edges")
        row = col.row()
        row.active = md.use_crease
        row.prop(md, "crease_weight", text="Crease Weight")

        col = split.column()

        col.prop(md, "offset")
        col.prop(md, "use_even_offset", text="Even Thickness")
        col.prop(md, "use_relative_offset", text="Relative Thickness")
        col.prop(md, "use_boundary", text="Boundary")
        col.prop(md, "use_replace", text="Replace Original")

        col.prop(md, "material_offset", text="Material Offset")

    def DATA_TRANSFER(self, layout, ob, md):
        row = layout.row(align=True)
        row.prop(md, "object")
        sub = row.row(align=True)
        sub.active = bool(md.object)
        sub.prop(md, "use_object_transform", text="", icon='GROUP')

        layout.separator()

        split = layout.split(factor=0.333)
        split.prop(md, "use_vert_data")
        use_vert = md.use_vert_data
        row = split.row()
        row.active = use_vert
        row.prop(md, "vert_mapping", text="")
        if use_vert:
            col = layout.column(align=True)
            split = col.split(factor=0.333, align=True)
            sub = split.column(align=True)
            sub.prop(md, "data_types_verts")
            sub = split.column(align=True)
            row = sub.row(align=True)
            row.prop(md, "layers_vgroup_select_src", text="")
            row.label(icon='RIGHTARROW')
            row.prop(md, "layers_vgroup_select_dst", text="")
            row = sub.row(align=True)
            row.label(text="", icon='NONE')

        layout.separator()

        split = layout.split(factor=0.333)
        split.prop(md, "use_edge_data")
        use_edge = md.use_edge_data
        row = split.row()
        row.active = use_edge
        row.prop(md, "edge_mapping", text="")
        if use_edge:
            col = layout.column(align=True)
            split = col.split(factor=0.333, align=True)
            sub = split.column(align=True)
            sub.prop(md, "data_types_edges")

        layout.separator()

        split = layout.split(factor=0.333)
        split.prop(md, "use_loop_data")
        use_loop = md.use_loop_data
        row = split.row()
        row.active = use_loop
        row.prop(md, "loop_mapping", text="")
        if use_loop:
            col = layout.column(align=True)
            split = col.split(factor=0.333, align=True)
            sub = split.column(align=True)
            sub.prop(md, "data_types_loops")
            sub = split.column(align=True)
            row = sub.row(align=True)
            row.label(text="", icon='NONE')
            row = sub.row(align=True)
            row.prop(md, "layers_vcol_select_src", text="")
            row.label(icon='RIGHTARROW')
            row.prop(md, "layers_vcol_select_dst", text="")
            row = sub.row(align=True)
            row.prop(md, "layers_uv_select_src", text="")
            row.label(icon='RIGHTARROW')
            row.prop(md, "layers_uv_select_dst", text="")
            col.prop(md, "islands_precision")

        layout.separator()

        split = layout.split(factor=0.333)
        split.prop(md, "use_poly_data")
        use_poly = md.use_poly_data
        row = split.row()
        row.active = use_poly
        row.prop(md, "poly_mapping", text="")
        if use_poly:
            col = layout.column(align=True)
            split = col.split(factor=0.333, align=True)
            sub = split.column(align=True)
            sub.prop(md, "data_types_polys")

        layout.separator()

        split = layout.split()
        col = split.column()
        row = col.row(align=True)
        sub = row.row(align=True)
        sub.active = md.use_max_distance
        sub.prop(md, "max_distance")
        row.prop(md, "use_max_distance", text="", icon='STYLUS_PRESSURE')

        col = split.column()
        col.prop(md, "ray_radius")

        layout.separator()

        split = layout.split()
        col = split.column()
        col.prop(md, "mix_mode")
        col.prop(md, "mix_factor")

        col = split.column()
        row = col.row()
        row.active = bool(md.object)
        row.operator("object.datalayout_transfer", text="Generate Data Layers")
        row = col.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        sub = row.row(align=True)
        sub.active = bool(md.vertex_group)
        sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

    def NORMAL_EDIT(self, layout, ob, md):
        has_vgroup = bool(md.vertex_group)
        do_polynors_fix = not md.no_polynors_fix
        needs_object_offset = (((md.mode == 'RADIAL') and not md.target) or
                               ((md.mode == 'DIRECTIONAL') and md.use_direction_parallel))

        row = layout.row()
        row.prop(md, "mode", expand=True)

        split = layout.split()

        col = split.column()
        col.prop(md, "target", text="")
        sub = col.column(align=True)
        sub.active = needs_object_offset
        sub.prop(md, "offset")
        row = col.row(align=True)

        col = split.column()
        row = col.row()
        row.active = (md.mode == 'DIRECTIONAL')
        row.prop(md, "use_direction_parallel")

        subcol = col.column(align=True)
        subcol.label(text="Mix Mode:")
        subcol.prop(md, "mix_mode", text="")
        subcol.prop(md, "mix_factor")
        row = subcol.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        sub = row.row(align=True)
        sub.active = has_vgroup
        sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
        row = subcol.row(align=True)
        row.prop(md, "mix_limit")
        row.prop(md, "no_polynors_fix", text="", icon='UNLOCKED' if do_polynors_fix else 'LOCKED')

    def CORRECTIVE_SMOOTH(self, layout, ob, md):
        is_bind = md.is_bind

        layout.prop(md, "factor", text="Factor")
        layout.prop(md, "iterations")

        row = layout.row()
        row.prop(md, "smooth_type")

        split = layout.split()

        col = split.column()
        col.label(text="Vertex Group:")
        row = col.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

        col = split.column()
        col.prop(md, "use_only_smooth")
        col.prop(md, "use_pin_boundary")

        layout.prop(md, "rest_source")
        if md.rest_source == 'BIND':
            layout.operator("object.correctivesmooth_bind", text="Unbind" if is_bind else "Bind")

    def WEIGHTED_NORMAL(self, layout, ob, md):
        layout.label(text="Weighting Mode:")
        split = layout.split(align=True)
        col = split.column(align=True)
        col.prop(md, "mode", text="")
        col.prop(md, "weight", text="Weight")
        col.prop(md, "keep_sharp")

        col = split.column(align=True)
        row = col.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        row.active = bool(md.vertex_group)
        row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
        col.prop(md, "thresh", text="Threshold")
        col.prop(md, "face_influence")




classes = (
    HP_MT_popup_properties,

)
register, unregister = bpy.utils.register_classes_factory(classes)


if __name__ == "__main__":
    register()
