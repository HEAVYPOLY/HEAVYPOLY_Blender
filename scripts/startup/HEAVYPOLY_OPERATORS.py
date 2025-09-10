bl_info = {
    "name": "Heavypoly Operators",
    "description": "Operators that make for smooth blending",
    "author": "Vaughan Ling",
    "version": (0, 1, 0),
    "blender": (4, 0, 0),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "category": "Operators"
    }

import bpy
import bmesh
from bpy.types import Menu
from bpy.types import Operator
from bpy.props import BoolProperty
from mathutils import Color

class HP_OT_unhide(bpy.types.Operator):
    bl_idname = "mesh.hp_unhide"         # unique identifier for buttons and menu items to reference.
    bl_label = "Unhide and keep selection"       # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def execute(self, context):
        ## 1 Save selection
        bpy.ops.object.vertex_group_add()
        bpy.ops.object.vertex_group_assign()
        ## 2 Unhide
        bpy.ops.mesh.reveal()
        ## 3 Deselect all
        bpy.ops.mesh.select_all(action='DESELECT')
        ## 4 Recall selection
        bpy.ops.object.vertex_group_select()
        bpy.ops.object.vertex_group_remove(all=False, all_unlocked=False)
        return {'FINISHED'}

class HP_OT_loopcut(bpy.types.Operator):
    bl_idname = "mesh.hp_loopcut"         # unique identifier for buttons and menu items to reference.
    bl_label = "Loopcut with tablet modals"       # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.


    def modal(self, context, event):
        if event.type == 'MOUSEMOVE' and event.value == 'PRESS':
            print('Mousemove...')
            bpy.ops.mesh.loopcut_slide('INVOKE_DEFAULT')
            return {'RUNNING_MODAL'}
        if event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
            return {'CANCELLED'}
        elif event.type == 'MOUSEMOVE' and event.value == 'RELEASE':
            bpy.context.scene.tool_settings.mesh_select_mode = (False, True, False)
            print('Release...')
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}
    def invoke(self, context, event):

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

class HP_OT_smart_snap_cursor(bpy.types.Operator):
    bl_idname = "view3d.smart_snap_cursor"        # unique identifier for buttons and menu items to reference.
    bl_label = ""         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    def invoke(self, context, event):
        try:
            if context.active_object.mode == 'EDIT':
                if context.active_object.type == 'MESH':
                    if  context.object.data.total_vert_sel == 0:
                        bpy.ops.view3d.snap_cursor_to_center()
                    else:
                        bpy.ops.view3d.snap_cursor_to_selected()
                else:
                    bpy.ops.view3d.snap_cursor_to_selected()
            elif len(bpy.context.selected_objects) > 0:
                bpy.ops.view3d.snap_cursor_to_selected()
            else:
                bpy.ops.view3d.snap_cursor_to_center()
        except:
            bpy.ops.view3d.snap_cursor_to_center()
            #bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
        return {'FINISHED'}

class HP_OT_smart_snap_origin_collection(bpy.types.Operator):
    bl_idname = "view3d.smart_snap_origin_collection"        # unique identifier for buttons and menu items to reference.
    bl_label = "Smart Snap Origin Collection"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    def invoke(self, context, event):
        print('smartsnaporigincollection')
        try:
            if context.active_object.mode == 'EDIT':
                if context.active_object.type == 'MESH':
                    if  context.object.data.total_vert_sel == 0:
                        bpy.ops.view3d.snap_cursor_to_center()
                        bpy.ops.object.mode_set(mode='OBJECT')
                        bpy.ops.object.origin_set(type = 'ORIGIN_CURSOR')
                        bpy.ops.object.mode_set(mode='EDIT')
                    else:
                        bpy.ops.view3d.snap_cursor_to_selected()
                        bpy.ops.object.mode_set(mode='OBJECT')
                        bpy.ops.object.instance_offset_from_cursor()
                        bpy.ops.object.mode_set(mode='EDIT')
                else:
                    bpy.ops.view3d.snap_cursor_to_selected()
                    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                    bpy.ops.object.origin_set(type = 'ORIGIN_CURSOR')
                    #bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            elif len(bpy.context.selected_objects) > 0:
                bpy.ops.view3d.snap_cursor_to_selected()
                bpy.ops.object.instance_offset_from_cursor()
            else:
                #bpy.ops.view3d.snap_cursor_to_center()
                #bpy.ops.object.origin_set(type = 'ORIGIN_CURSOR')
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            #bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
        except:
            return {'FINISHED'}
        return {'FINISHED'}
class HP_OT_smart_snap_origin(bpy.types.Operator):
    bl_idname = "view3d.smart_snap_origin"        # unique identifier for buttons and menu items to reference.
    bl_label = ""         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    def invoke(self, context, event):
        print('smartsnaporigin')
        cursor_start_location = bpy.context.scene.cursor.location * 1
        # print(cursor_start_location)
        try:
            if context.active_object.mode == 'EDIT':
                if context.active_object.type == 'MESH':
                    if  context.object.data.total_vert_sel == 0:
                        bpy.ops.view3d.snap_cursor_to_center()
                        bpy.ops.object.mode_set(mode='OBJECT')
                        bpy.ops.object.origin_set(type = 'ORIGIN_CURSOR')
                        bpy.ops.object.mode_set(mode='EDIT')
                    else:
                        bpy.ops.view3d.snap_cursor_to_selected()
                        bpy.ops.object.mode_set(mode='OBJECT')
                        bpy.ops.object.origin_set(type = 'ORIGIN_CURSOR')
                        bpy.ops.object.mode_set(mode='EDIT')
                else:
                    bpy.ops.view3d.snap_cursor_to_selected()
                    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                    bpy.ops.object.origin_set(type = 'ORIGIN_CURSOR')
                    #bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            elif len(bpy.context.selected_objects) > 0:
                bpy.ops.object.origin_set(type = 'ORIGIN_GEOMETRY')
            else:
                #bpy.ops.view3d.snap_cursor_to_center()
                #bpy.ops.object.origin_set(type = 'ORIGIN_CURSOR')
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            #bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
            print(cursor_start_location)
            bpy.context.scene.cursor.location = (cursor_start_location[0],cursor_start_location[1],cursor_start_location[2])
        except:
            return {'FINISHED'}
        return {'FINISHED'}

class HP_OT_duplicate_move(bpy.types.Operator):
    bl_idname = "view3d.hp_duplicate_move"
    bl_label = ""
    bl_options = {'REGISTER'}
    def invoke(self, context, event):
        if context.active_object.mode == 'OBJECT':
            bpy.ops.object.duplicate('INVOKE_DEFAULT', False)
            bpy.ops.transform.translate('INVOKE_DEFAULT', False)

        if context.active_object.mode == 'EDIT':
            bpy.ops.mesh.duplicate('INVOKE_DEFAULT', False)
            bpy.ops.transform.translate('INVOKE_DEFAULT', False)

        return {'FINISHED'}



class HP_OT_PushAndSlide(bpy.types.Operator):
    bl_idname = "mesh.push_and_slide"        # unique identifier for buttons and menu items to reference.
    bl_label = "Push And Slide"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def invoke(self, context, event):
        if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (True, False, False):
            bpy.ops.transform.vert_slide('INVOKE_DEFAULT', mirror=False, correct_uv=True)
        elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, False, True):
            bpy.ops.transform.shrink_fatten('INVOKE_DEFAULT', use_even_offset=True, mirror=False)
        else:
            bpy.ops.transform.edge_slide('INVOKE_DEFAULT', mirror=False, correct_uv=True)
        return {'FINISHED'}


class HP_OT_extrude(Operator):
    bl_label = "Context Sensitive Extrude"
    bl_idname = "mesh.hp_extrude"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj is not None and obj.mode == 'EDIT')

    def invoke(self, context, event):
        if bpy.context.object.type == 'CURVE':
            bpy.ops.curve.extrude()
            bpy.ops.transform.translate('INVOKE_DEFAULT')
            return {'FINISHED'}

        mesh = context.object.data
        selface = mesh.total_face_sel
        seledge = mesh.total_edge_sel
        selvert = mesh.total_vert_sel

        if selvert == 0:
            bpy.ops.mesh.select_mode(type='VERT')
            bpy.ops.mesh.dupli_extrude_cursor('INVOKE_DEFAULT')
            return {'FINISHED'}
        if selvert > 0 and seledge == 0:
            bpy.ops.mesh.extrude_region_move('INVOKE_DEFAULT')
            return {'FINISHED'}
        if seledge > 0 and selface == 0:
            bpy.ops.mesh.extrude_region_move('INVOKE_DEFAULT')
            return {'FINISHED'}

        bpy.ops.mesh.extrude_region_move('EXEC_DEFAULT')

        if mesh.total_face_sel != selface:
            bpy.ops.transform.shrink_fatten('INVOKE_DEFAULT', use_even_offset=True)
            return {'FINISHED'}

        bpy.ops.transform.shrink_fatten('INVOKE_DEFAULT', use_even_offset=True)
        return {'FINISHED'}

    

class HP_OT_SmartScale(Operator):
    bl_idname = "view3d.smart_scale"        # unique identifier for buttons and menu items to reference.
    bl_label = "Context Sensitive Scale"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    # @classmethod
    # def poll(cls, context):
        # obj = context.active_object
        # return (obj is not None and obj.mode == 'OBJECT')
    def invoke(self, context, event):
        modal = False
        try:
            for ob in bpy.context.selected_objects:
                if ob.mode == 'OBJECT' and ob.children == () and ob.data.users == 1 and ob.type == 'MESH':
                    modal = True
                    print('running modal')
        except:
            pass
        if modal:
            context.window_manager.modal_handler_add(self)
            print('Scaling MODAL')
        bpy.ops.transform.resize('INVOKE_DEFAULT', mirror=True)
        return {'RUNNING_MODAL'}
    def modal(self, context, event):
        print("MODAL " + event.type)
        if event.type == 'MOUSEMOVE':
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            return {'FINISHED'}
        # if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
        #     print('Applying Scale')
        #     return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}
        else:
            return {'RUNNING_MODAL'}
class HP_OT_SmartBevel(bpy.types.Operator):
    bl_idname = "view3d.smart_bevel"        # unique identifier for buttons and menu items to reference.
    bl_label = "Smart Bevel"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def invoke(self, context, event):
        if context.active_object.mode == 'OBJECT':
            print('Only works in Edit Mode')
            #bpy.ops.view3d.hp_draw('INVOKE_DEFAULT')
        else:
            me = bpy.context.object.data
            bm = bmesh.from_edit_mesh(me)
            sel = []
            for v in bm.verts:
                if v.select:
                    sel.append(v)
            if len(sel) == 0:
                print('Nothing Selected')
                # bpy.ops.view3d.hp_draw('INVOKE_DEFAULT')
            else:
                if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (True, False, False):
                    bpy.ops.mesh.bevel('INVOKE_DEFAULT',clamp_overlap=True,affect='VERTICES')
                    return {'FINISHED'}
                elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, False, True):
                    bpy.ops.mesh.select_mode(type = 'EDGE')
                    print('edge mode...')
                    bpy.ops.mesh.region_to_loop('INVOKE_DEFAULT')
                    print('selecting border...')
                    me = bpy.context.object.data
                    bm = bmesh.from_edit_mesh(me)
                    sel = []
                    for v in bm.verts:
                        if v.select:
                            sel.append(v)
                    if len(sel) == 0:
                        bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.bevel('INVOKE_DEFAULT', clamp_overlap=True, miter_outer='ARC')
            bpy.ops.mesh.remove_doubles()

        return {'FINISHED'}




class HP_OT_SeparateAndSelect(bpy.types.Operator):
    bl_idname = "object.separate_and_select"        # unique identifier for buttons and menu items to reference.
    bl_label = "Separate and Select"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    def execute(self, context):

        bases = bpy.context.selected_objects
        if bpy.context.object.type == 'MESH':
            bpy.ops.mesh.separate(type='SELECTED')
        elif bpy.context.object.type == 'GPENCIL':
            bpy.ops.gpencil.stroke_separate(mode='POINT')
        elif bpy.context.object.type == 'GREASEPENCIL':
            bpy.ops.grease_pencil.stroke_separate(mode='POINT')

            # bpy.ops.gpencil.stroke_split()
        elif bpy.context.object.type == 'CURVE':
            bpy.ops.curve.separate()
        if bpy.context.object.type == 'GPENCIL':
            bpy.ops.gpencil.editmode_toggle()
        elif bpy.context.object.type == 'GREASEPENCIL':
            bpy.ops.object.mode_set('EDIT', toggle=True)
        else:
            bpy.ops.object.editmode_toggle()
            
        for b in bases:
            b.select_set(state=False)
        selected = bpy.context.selected_objects
        bpy.context.view_layer.objects.active = selected[-1]
        if bpy.context.object.type == 'GPENCIL':
            bpy.ops.gpencil.editmode_toggle()
        elif bpy.context.object.type == 'GREASEPENCIL':
            bpy.ops.grease_pencil.editmode_toggle()
        else:
            bpy.ops.object.editmode_toggle()
        if bpy.context.object.type == 'MESH':
            bpy.ops.mesh.select_all(action='SELECT')
        if bpy.context.object.type == 'CURVE':
            bpy.ops.curve.select_all(action='SELECT')
        return {'FINISHED'}

class HP_OT_SmartShadeSmooth(bpy.types.Operator):
    bl_idname = "view3d.smart_shade_smooth_toggle"        # unique identifier for buttons and menu items to reference.
    bl_label = "Smart Shade Smooth"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def invoke(self, context, event):
        isedit = False
        for ob in bpy.context.selected_objects:
            if ob.type == 'MESH':
                if ob.mode == 'EDIT':
                    isedit = True
                    bpy.ops.object.editmode_toggle()
                bpy.ops.object.shade_smooth()
                ob.data.use_auto_smooth = True
                ob.data.auto_smooth_angle = 0.436332
                if isedit:
                    bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

class HP_OT_toggle_render_material(bpy.types.Operator):
    bl_idname = "view3d.toggle_render_material"        # unique identifier for buttons and menu items to reference.
    bl_label = ""         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def invoke(self, context, event):
        if bpy.context.space_data.viewport_shade != 'MATERIAL':
            bpy.context.space_data.viewport_shade = 'MATERIAL'
        elif bpy.context.space_data.viewport_shade == 'MATERIAL':
            bpy.context.space_data.viewport_shade = 'RENDERED'
        return {'FINISHED'}



class HP_OT_Smart_Delete(bpy.types.Operator):
    bl_idname = "view3d.smart_delete"
    bl_label = "Smart Delete"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        obj = context.object
        objType = getattr(obj, 'type', '')
        act = bpy.context.active_object

        try:
            if not act:
                for o in bpy.context.selected_objects:
                    bpy.context.view_layer.objects.active = o
                    act = bpy.context.active_object

            actname = act.name if act else ""

            # Object mode deletion logic
            if context.active_object.mode == 'OBJECT':
                if '_Cutter' in actname:
                    bpy.ops.object.delete(use_global=False)
                    for obj in bpy.context.view_layer.objects:
                        bpy.context.view_layer.objects.active = obj
                        bpy.ops.object.modifier_remove(modifier=actname)
                else:
                    bpy.ops.object.delete(use_global=False)

            # Edit mode deletion for different object types
            elif objType == 'CURVE':
                if context.active_object.mode != 'OBJECT':
                    bpy.ops.curve.delete(type='VERT')

            # Grease Pencil handling (GPENCIL for 4.2, GREASEPENCIL for 4.3+)
            elif objType in {'GPENCIL', 'GREASEPENCIL'}:
                if context.active_object.mode != 'OBJECT':
                    if bpy.app.version < (4, 3, 0):
                        bpy.ops.gpencil.delete(type='POINTS')
                    else:
                        # Blender 4.3+ Grease Pencil API handling
                        bpy.ops.grease_pencil.delete()

            # Meta object handling
            elif objType == 'META':
                if context.active_object.mode != 'OBJECT':
                    bpy.ops.mball.delete_metaelems()

            # Mesh handling
            elif objType == 'MESH':
                if context.active_object.mode != 'OBJECT':
                    if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, False, True):
                        bpy.ops.mesh.delete(type='FACE')
                    else:
                        bpy.ops.mesh.delete(type='VERT')

        except Exception as e:
            print(f"Error in Smart Delete: {e}")
        
        return {'FINISHED'}







class HP_OT_Subdivision_Toggle(bpy.types.Operator):
    bl_idname = "view3d.subdivision_toggle"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):

        for o in bpy.context.selected_objects:
            bpy.context.view_layer.objects.active = o
            if 0 < len([m for m in bpy.context.object.modifiers if m.type == "SUBSURF"]):
                if bpy.context.object.modifiers["Subsurf_Base"].show_viewport == False:
                    bpy.context.object.modifiers["Subsurf_Base"].show_render = True
                    bpy.context.object.modifiers["Subsurf_Base"].show_viewport = True
                else:
                    bpy.context.object.modifiers["Subsurf_Base"].show_render = False
                    bpy.context.object.modifiers["Subsurf_Base"].show_viewport = False

            else:
                o.modifiers.new("Subsurf_Base", "SUBSURF")
                bpy.context.object.modifiers["Subsurf_Base"].name = "Subsurf_Base"
                bpy.context.object.modifiers["Subsurf_Base"].render_levels = 3
                bpy.context.object.modifiers["Subsurf_Base"].levels = 3
                bpy.context.object.modifiers["Subsurf_Base"].show_in_editmode = True
                bpy.context.object.modifiers["Subsurf_Base"].show_on_cage = False
                bpy.context.object.modifiers["Subsurf_Base"].subdivision_type = 'CATMULL_CLARK'

        return {'FINISHED'}

class HP_OT_SaveWithoutPrompt(bpy.types.Operator):
    bl_idname = "wm.save_without_prompt"
    bl_label = "Save without prompt"

    def execute(self, context):
        bpy.ops.wm.save_mainfile()
        return {'FINISHED'}
class HP_OT_RevertWithoutPrompt(bpy.types.Operator):
    bl_idname = "wm.revert_without_prompt"
    bl_label = "Revert without prompt"

    def execute(self, context):
        bpy.ops.wm.revert_mainfile()
        return {'FINISHED'}
class HP_OT_DeleteWithoutPrompt(bpy.types.Operator):
    bl_idname = "wm.delete_without_prompt"
    bl_label = "Delete without prompt"

    def execute(self, context):
        bpy.ops.object.delete()
        return {'FINISHED'}


class HP_OT_SetCollectionCenter(bpy.types.Operator):
    bl_idname = "view3d.hp_set_collection_center"         # unique identifier for buttons and menu items to reference.
    bl_label = "Set Collection Center"       # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def execute(self, context):
        ## 1 Save selection
        bpy.ops.view3d.snap_cursor_to_selected()
        #bpy.ops.view3d.snap_cursor_to_selected()
       # bpy.ops.object.instance_offset_from_cursor()
        return {'FINISHED'}

#### MOVE SPACE Y AXIS #####


class HP_TranslateModalOperator(bpy.types.Operator):
    """Toggle Move Mode and Y Constraint"""
    bl_idname = "object.modal_translate"
    bl_label = "Modal Translate"
    bl_options = {'REGISTER', 'UNDO'}

    is_moving: bpy.props.BoolProperty(default=False)
    constrain_y: bpy.props.BoolProperty(default=False)

    def modal(self, context, event):
        # Listen for keypresses
        if event.type == 'SPACE' and event.value == 'PRESS':
            # Toggle Y-axis constraint
            self.constrain_y = not self.constrain_y
            self.report({'INFO'}, f"Y-axis constraint {'enabled' if self.constrain_y else 'disabled'}")
            
            # Restart the transform operator with updated constraints
            bpy.ops.transform.translate(
                'INVOKE_DEFAULT',
                constraint_axis=(False, self.constrain_y, False)  # X, Y, Z constraints
            )
            return {'RUNNING_MODAL'}

        if event.type in {'LEFTMOUSE', 'RET'}:  # Confirm operation
            self.report({'INFO'}, "Transform Confirmed")
            self.is_moving = False
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel operation
            self.report({'INFO'}, "Transform Canceled")
            self.is_moving = False
            bpy.ops.ed.undo()  # Undo the transform
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        # Start the transform operator
        self.is_moving = True
        self.constrain_y = False  # Default: no constraint
        bpy.ops.transform.translate('INVOKE_DEFAULT')

        # Add a modal handler for post-transform actions
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

class OBJECT_OT_set_camera_off_wire(bpy.types.Operator):
    """Turn OFF Camera Visibility, Display as WIRE, Shadow ON"""
    bl_idname = "object.set_camera_off_wire"
    bl_label = "Hide From Camera (Wire Display)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.selected_objects

    def execute(self, context):
        is_cycles = context.scene.render.engine == 'CYCLES'
        for obj in context.selected_objects:
            if hasattr(obj, "visible_camera"):
                obj.visible_camera = False
            if is_cycles and hasattr(obj, "visible_shadow"):
                obj.visible_shadow = True
            obj.display_type = 'WIRE'
        self.report({'INFO'}, "Camera visibility OFF, Display as WIRE.")
        return {'FINISHED'}

class OBJECT_OT_set_camera_on_textured(bpy.types.Operator):
    """Turn ON Camera Visibility, Display as TEXTURED"""
    bl_idname = "object.set_camera_on_textured"
    bl_label = "Show in Camera (Textured Display)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.selected_objects

    def execute(self, context):
        for obj in context.selected_objects:
            if hasattr(obj, "visible_camera"):
                obj.visible_camera = True
            obj.display_type = 'TEXTURED'
        self.report({'INFO'}, "Camera visibility ON, Display as TEXTURED.")
        return {'FINISHED'}

class OBJECT_OT_select_camera_hidden(bpy.types.Operator):
    """Select all geometry objects with Camera Visibility OFF"""
    bl_idname = "object.select_camera_hidden"
    bl_label = "Select Hidden From Camera"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        count = 0
        geometry_types = {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT'}

        for obj in context.scene.objects:
            if (
                obj.type in geometry_types
                and hasattr(obj, "visible_camera")
                and not obj.visible_camera
            ):
                obj.select_set(True)
                count += 1

        self.report({'INFO'}, f"Selected {count} camera-hidden geometry objects.")
        return {'FINISHED'}




def draw_func(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("object.set_camera_off_wire", icon='HIDE_ON')
    layout.operator("object.set_camera_on_textured", icon='HIDE_OFF')
    layout.operator("object.select_camera_hidden", icon='RESTRICT_VIEW_ON')


classes = (
    HP_OT_SaveWithoutPrompt,
    HP_OT_RevertWithoutPrompt,
    HP_OT_DeleteWithoutPrompt,
    HP_OT_duplicate_move,
    HP_OT_Subdivision_Toggle,
    HP_OT_Smart_Delete,
    HP_OT_SmartShadeSmooth,
    HP_OT_SeparateAndSelect,
    HP_OT_PushAndSlide,
    HP_OT_SmartBevel,
    HP_OT_smart_snap_cursor,
    HP_OT_smart_snap_origin,
    HP_OT_smart_snap_origin_collection,
    HP_OT_extrude,
    HP_OT_loopcut,
    HP_OT_SmartScale,
    HP_OT_unhide,
    HP_OT_SetCollectionCenter,
    HP_TranslateModalOperator,
    OBJECT_OT_set_camera_off_wire,
    OBJECT_OT_set_camera_on_textured,
    OBJECT_OT_select_camera_hidden,

)
#register, unregister = bpy.utils.register_classes_factory(classes)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_func)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_func)

if __name__ == "__main__":
    register()