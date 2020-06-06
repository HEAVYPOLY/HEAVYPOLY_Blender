import bpy
import random
from bpy.props import *
from bpy_extras.node_utils import find_node_input
class HP_MT_popup_materials(bpy.types.Operator):
    bl_idname = "popup.hp_materials"
    bl_label = "Heavypoly Material Popup"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        ob = context.object
        wm = context.window_manager
        
        # return bpy.context.window_manager.popup_menu(
        return wm.invoke_popup(self, width=400)
    def check(self, context):
        return True
    # @classmethod
    # def poll(cls, context):
        # return (context.object) and CyclesButtonsPanel.poll(context)
        # return (context.material or context.object) and CyclesButtonsPanel.poll(context)
    # def find_node_input(node, name):
        # for input in node.inputs:
            # if input.name == name:
                # return input
        # return None
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = row.column(align=True)
        col2 = row.column(align=True)
        col2.operator('popup.hp_render',icon='NONE',text='Render Settings')
        col2.separator()
         #Vertex Color
        ob = context.object
        box = col.box()
        box.label(text = 'MATERIAL LIBRARY')
        box.template_ID(ob, "active_material")
        # box.template_ID(self.paint_settings(context), "palette", new="palette.new")



    #    def poll(cls, context):
    #        settings = cls.paint_settings(context)
    #        brush = settings.brush
    #        if context.image_paint_object:
    #            capabilities = brush.image_paint_capabilities
    #            return capabilities.has_color

    #        elif context.vertex_paint_object:
    #            capabilities = brush.vertex_paint_capabilities
    #            return capabilities.has_color


        # layout = self.layout
        # settings = self.paint_settings(context)

        # box.template_ID(settings, "palette", new="palette.new")
        # if settings.palette:
        #     layout.template_palette(settings, "palette", color=True)




#       col.template_list("", "vcols", me, "vertex_colors", me.vertex_colors, "active_index", rows=1)
#        col.operator("mesh.vertex_color_add", icon='ZOOMIN', text="")
#        col.operator("mesh.vertex_color_remove", icon='ZOOMOUT', text="")
        col.separator()
        #Material Slots
        rows=6

        actob = context.active_object
        box = col.box()
        box.label(text = 'MATERIAL SLOTS')
        row = box.row()

        sub = row.column()
        sub.template_list("MATERIAL_UL_matslots", "", ob, "material_slots", ob, "active_material_index", rows=rows)
        sub = row.column()


        sub.operator("3dview.material_slot_add", icon='ADD', text="")
        sub.operator("3dview.material_slot_remove", icon='REMOVE', text="")
        sub.operator("object.material_slot_move", icon='TRIA_UP', text="").direction='UP'
        sub.operator("object.material_slot_move", icon='TRIA_DOWN', text="").direction='DOWN'
        box.operator("object.material_slot_assign", text="Assign Selection to Slot")

        col.separator()


        if actob.type == 'GPENCIL':
            col.operator('gpencil.stroke_change_color', icon='NONE', text='Apply')
        else:
            col.operator('3dview.material_new', icon='NONE', text='New Material')
        col.operator('3dview.material_copy', icon='NONE', text='Duplicate Material')
        col.operator('3dview.material_delete', icon='NONE', text='Delete Material')

        # if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, False, True):
            # col.operator("mesh.select_similar", text='Select Elements by Slot').type = 'MATERIAL'
        mat = bpy.context.object.active_material







        col.separator()
#        col.prop(mat, "blend_method",text='')
        # col.prop(mat, "shadow_method",text='')
        if mat != None:
            col.prop(mat, "refraction_depth",text='')
            col.row().prop(mat, "use_screen_refraction")
            col.row().prop(mat, "use_sss_translucency")
            col.separator()
        else:
            print('No Material Selected')
        col.label(text = 'VERTEX COLOR (for _V materials)')
        ts = context.tool_settings
        ups = ts.unified_paint_settings
        ptr = ups if ups.use_unified_color else ts.vertex_paint.brush
        col.template_color_picker(ptr, 'color', value_slider=True)
        col.prop(ptr, 'color', text='')

        if bpy.context.object.type == 'MESH':
            col.operator("mesh.material_apply", text='Apply Vertex Color')
            col.operator("mesh.select_vertex_color", text='Select by Vertex Color')
            col.operator("ui.eyedropper_id", text='Eyedropper')

            me = bpy.context.active_object.data
            col.template_list("MESH_UL_vcols", "vcols", me, "vertex_colors", me.vertex_colors, "active_index", rows=1)
        col.separator()

        #Nodes

        if bpy.context.object.type in ['MESH','CURVE']:
            # box = col2.box()
            # sub = box.column(align=True)
            # ntree = bpy.context.object.active_material.node_tree
            # node = ntree.get_output_node('EEVEE')
            # if node:
                # input = find_node_input(node, 'Surface')
                # inputvolume = find_node_input(node, 'Volume')
                # inputdisplacement = find_node_input(node, 'Displacement')
                # if input:
                    # sub.template_node_view(ntree, node, input)
                # if inputvolume:
                    # sub.template_node_view(ntree, node, inputvolume)
                # if inputdisplacement:
                    # sub.template_node_view(ntree, node, inputdisplacement)

                # else:
                    # sub.label(text="Incompatible output node")
            # else:
                # sub.label(text="No output node")
            if mat != None:
                actnode = bpy.context.active_object.active_material.node_tree.nodes.active
                print(actnode)
                col2.prop(actnode, 'type', text='Shader')
                for x in bpy.context.active_object.active_material.node_tree.nodes.active.inputs:
                    if x.name != 'Normal' and x.name != 'Clearcoat Normal' and x.name != 'Tangent':
                        col2.prop(x,'default_value', text = x.name)




####Grease Pencil Material Props
        ma = bpy.context.object.active_material
        if ma is not None and ma.grease_pencil is not None:
            gpcolor = ma.grease_pencil
            col2.label(text='                               ++STROKE++')
            col2.active = not gpcolor.lock
            col2.operator('3dview.gp_stroketoggle', text='Toggle Stroke')
            col2.prop(gpcolor, "mode", text="")
            col2.prop(gpcolor, "stroke_style", text="")
            if gpcolor.stroke_style == 'TEXTURE':
                row = col2.row()
                row.enabled = not gpcolor.lock
                col = row.column(align=True)
                col.template_ID(gpcolor, "stroke_image", open="image.open")
                col.prop(gpcolor, "pixel_size", text="UV Factor")
                col.prop(gpcolor, "use_stroke_pattern", text="Use As Pattern")
            if gpcolor.stroke_style == 'SOLID' or gpcolor.use_stroke_pattern is True:
                col2.prop(gpcolor, "color", text="")
            col2.label(text='')
            col2.active = not gpcolor.lock
            col2.label(text='                                 ++FILL++')
            col2.operator('3dview.gp_filltoggle', text='Toggle Fill')
            col2.prop(gpcolor, "fill_style", text="")
            if gpcolor.fill_style == 'GRADIENT':
                col2.prop(gpcolor, "gradient_type", text="")
            if gpcolor.fill_style != 'TEXTURE':
                col2.prop(gpcolor, "fill_color", text="")
                if gpcolor.fill_style in {'GRADIENT', 'CHESSBOARD'}:
                    col2.prop(gpcolor, "mix_color", text="")
                if gpcolor.fill_style == 'GRADIENT':
                    col2.prop(gpcolor, "mix_factor", text="Gradient Mix")
                if gpcolor.fill_style in {'GRADIENT', 'CHESSBOARD'}:
                    col2.prop(gpcolor, "flip", text="Flip Colors")
                    col2.prop(gpcolor, "pattern_shift", text="Location")
                    col2.prop(gpcolor, "pattern_scale", text="Scale")
                if gpcolor.gradient_type == 'RADIAL' and gpcolor.fill_style not in {'SOLID', 'CHESSBOARD'}:
                    col2.prop(gpcolor, "pattern_radius", text="Radius")
                else:
                    if gpcolor.fill_style != 'SOLID':
                        col2.prop(gpcolor, "pattern_angle", text="Angle")
                if gpcolor.fill_style == 'CHESSBOARD':
                    col2.prop(gpcolor, "pattern_gridsize", text="Box Size")

            # Texture
            if gpcolor.fill_style == 'TEXTURE' or (gpcolor.texture_mix is True and gpcolor.fill_style == 'SOLID'):
                col2.template_ID(gpcolor, "fill_image", open="image.open")
                if gpcolor.fill_style == 'TEXTURE':
                    col2.prop(gpcolor, "use_fill_pattern", text="Use As Pattern")
                    if gpcolor.use_fill_pattern is True:
                        col2.prop(gpcolor, "fill_color", text="Color")
                col2.prop(gpcolor, "texture_offset", text="Offset")
                col2.prop(gpcolor, "texture_scale", text="Scale")
                col2.prop(gpcolor, "texture_angle")
                col2.prop(gpcolor, "texture_opacity")
                col2.prop(gpcolor, "texture_clamp", text="Clip Image")
                if gpcolor.use_fill_pattern is False:
                    col2.prop(gpcolor, "texture_mix", text="Mix With Color")
                    if gpcolor.texture_mix is True:
                        col2.prop(gpcolor, "fill_color", text="Mix Color")
                        col2.prop(gpcolor, "mix_factor", text="Mix Factor", slider=True)


            col2.label(text='')
            col2.label(text='                                  /// LAYERS')
            gpd = context.gpencil_data
            row = col2.row()
            sub = row.column()
            layer_rows = 7
            sub.template_list("GPENCIL_UL_layer", "", gpd, "layers", gpd.layers, "active_index",
                              rows=layer_rows, reverse=True)
            sub = row.column()
            sub.operator("gpencil.layer_add", icon='ADD', text="")

            sub.operator("gpencil.layer_remove", icon='REMOVE', text="")
            sub.operator("gpencil.layer_move", icon='TRIA_UP', text="").type = 'UP'
            sub.operator("gpencil.layer_move", icon='TRIA_DOWN', text="").type = 'DOWN'
            sub.operator("gpencil.layer_merge", icon='TRIA_DOWN_BAR', text="")
            sub.operator("gpencil.layer_isolate", icon='GREASEPENCIL', text="").affect_visibility = False
            sub.operator("gpencil.layer_isolate", icon='RESTRICT_VIEW_OFF', text="").affect_visibility = True
            sub.menu("GPENCIL_MT_layer_specials", icon='ERROR', text="")
            gpl = context.active_gpencil_layer
            col2.prop(gpl, "opacity", text="Layer Opacity", slider=True)

class HP_OT_gp_stroke(bpy.types.Operator):
    bl_idname = '3dview.gp_type'
    bl_label = "Grease Pencil Type"
    def execute(self, context):
        bpy.context.object.active_material.grease_pencil.color[3] = 1
        bpy.context.object.active_material.grease_pencil.fill_color[3] = 0
        return {'FINISHED'}
class HP_OT_gp_stroketoggle(bpy.types.Operator):
    bl_idname = '3dview.gp_stroketoggle'
    bl_label = "Grease Pencil Stroke Toggle"
    def execute(self, context):
        if bpy.context.object.active_material.grease_pencil.color[3] < 1:
            bpy.context.object.active_material.grease_pencil.color[3] = 1
        else:
            bpy.context.object.active_material.grease_pencil.color[3] = 0
        return {'FINISHED'}
class HP_OT_gp_filltoggle(bpy.types.Operator):
    bl_idname = '3dview.gp_filltoggle'
    bl_label = "Grease Pencil Fill Toggle"
    def execute(self, context):
        if bpy.context.object.active_material.grease_pencil.fill_color[3] < 1:
            bpy.context.object.active_material.grease_pencil.fill_color[3] = 1
        else:
            bpy.context.object.active_material.grease_pencil.fill_color[3] = 0
        return {'FINISHED'}
class HP_OT_material_delete(bpy.types.Operator):
    bl_idname = '3dview.material_delete'
    bl_label = 'Delete Material'
    def execute(self, context):
        bpy.data.materials.remove(bpy.context.object.active_material)
        if context.active_object.mode != 'OBJECT' and context.active_object.type == 'MESH':
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.material_slot_remove()
            bpy.ops.object.editmode_toggle()
        else:
            bpy.ops.object.material_slot_remove()
        return {'FINISHED'}
class HP_OT_material_copy(bpy.types.Operator):
    bl_idname = '3dview.material_copy'
    bl_label = 'Copy Material'
    def execute(self, context):
        i = bpy.context.object.active_material_index
        newmat = bpy.context.active_object.active_material.copy()
        bpy.context.object.data.materials.append(newmat)
        bpy.context.object.active_material_index=len(bpy.context.object.data.materials)-1
        move = len(bpy.context.object.data.materials)-i-2
        for m in range(move):
            bpy.ops.object.material_slot_move(direction='UP')
        bpy.ops.object.material_slot_assign()
        return {'FINISHED'}

class HP_OT_material_slot_add(bpy.types.Operator):
    bl_idname = '3dview.material_slot_add'
    bl_label = 'Add Material Slot'
    def execute(self, context):
        i = bpy.context.object.active_material_index
        bpy.ops.object.material_slot_add()
        bpy.context.object.active_material_index=len(bpy.context.object.data.materials)-1
        move = len(bpy.context.object.data.materials)-i-2
        for m in range(move):
            bpy.ops.object.material_slot_move(direction='UP')
        bpy.ops.object.material_slot_assign()
        return {'FINISHED'}
class HP_OT_material_slot_remove(bpy.types.Operator):
    bl_idname = '3dview.material_slot_remove'
    bl_label = 'Remove Material Slot'
    def execute(self, context):
        if context.active_object.mode != 'OBJECT' and context.active_object.type == 'MESH':
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.material_slot_remove()
            bpy.ops.object.editmode_toggle()
        else:
            bpy.ops.object.material_slot_remove()
        return {'FINISHED'}
class HP_OT_material_new(bpy.types.Operator):
    bl_idname = '3dview.material_new'
    bl_label = 'Assign New Material'
    def execute(self, context):
        if bpy.context.object.active_material:
            print('Active Material - Creating New Slot')
            newmat = bpy.data.materials.new('Material')
            bpy.context.active_object.data.materials.append(newmat)
            bpy.context.object.active_material_index=len(bpy.context.object.data.materials)-1
            bpy.context.active_object.active_material.use_nodes=True
            bpy.ops.object.material_slot_assign()
        else:
            print('No Active Material')
            newmat = bpy.data.materials.new('Material')
            bpy.context.active_object.active_material = newmat
            bpy.context.active_object.active_material.use_nodes=True



        return {'FINISHED'}
class HP_OT_apply(bpy.types.Operator):
    bl_idname = "mesh.material_apply"        # unique identifier for buttons and menu items to reference.
    bl_label = "Fill Color"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    def execute(self, context):
        obj = bpy.context.object
        mesh = obj.data
        #if bpy.context.object.active_material.name.endswith('_V'):
        if context.active_object.mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.object.material_slot_assign()
            bpy.ops.object.editmode_toggle()
            return {'FINISHED'}
#        totface = mesh.total_face_sel
#        totedge = mesh.total_edge_sel
        totvert = mesh.total_vert_sel
        nothingselected = False
        if totvert == 0:
            nothingselected = True
            bpy.ops.mesh.select_all(action='SELECT')
        if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, False, True):
            bpy.ops.object.editmode_toggle()
            bpy.ops.paint.vertex_paint_toggle()
            bpy.context.object.data.use_paint_mask = True
            bpy.ops.paint.vertex_color_set()
            bpy.ops.object.editmode_toggle()
        else:
            bpy.ops.object.editmode_toggle()
            bpy.ops.paint.vertex_paint_toggle()
            bpy.context.object.data.use_paint_mask_vertex = True
            bpy.ops.paint.vertex_color_set()
            bpy.ops.object.editmode_toggle()

        bpy.ops.object.material_slot_assign()

        if nothingselected == True:
            bpy.ops.mesh.select_all(action='DESELECT')

        return {'FINISHED'}

class HP_OT_select_vertex_color(bpy.types.Operator):
    bl_idname = "mesh.select_vertex_color"        # unique identifier for buttons and menu items to reference.
    bl_label = "Select By Vertex Color"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    def execute(self, context):
        ob = bpy.context.object
        colors_list = []
        for ipoly in range(len(ob.data.polygons)):
            for ivertex in ob.data.polygons[ipoly].loop_indices:
                color_list = []
                for i in range(4):
                    color_list.append(str(ob.data.vertex_colors["Col"].data[ivertex].color[i]))
                colors_list.append(color_list)


        print(colors_list)
        return {'FINISHED'}

classes = (
    HP_MT_popup_materials,
    HP_OT_material_delete,
    HP_OT_material_copy,
    HP_OT_material_slot_add,
    HP_OT_material_slot_remove,
    HP_OT_material_new,
    HP_OT_apply,
    HP_OT_select_vertex_color,
    HP_OT_gp_stroketoggle,
    HP_OT_gp_filltoggle
)
register, unregister = bpy.utils.register_classes_factory(classes)


if __name__ == "__main__":
    register()
