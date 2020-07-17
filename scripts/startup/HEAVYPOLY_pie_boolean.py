bl_info = {
    "name": "HP Boolean Pie",
    "description": "",
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
#bpy.context.view_layer.objects.active
# Boolean Pie
class HP_MT_pie_boolean(Menu):
    bl_label = "HP Boolean"
    def draw(self, context):

        layout = self.layout
        pie = layout.menu_pie()
        split = pie.split()
        col = split.column(align=True)
        #Plain ol Booleans
        row = col.row(align=True)
        row.scale_y=1.5
        prop = row.operator("view3d.hp_boolean_live", text="Add")
        prop.bool_operation = 'UNION'
        prop.cutline = 'NO'
        prop.insetted = 'NO'
        prop.live = 'NO'
        prop.laser = 'NO'
        row = col.row(align=True)
        row.scale_y=1.5
        prop = row.operator("view3d.hp_boolean_live", text="Intersect")
        prop.bool_operation = 'INTERSECT'
        prop.cutline = 'NO'
        prop.insetted = 'NO'
        prop.live = 'NO'
        prop.laser = 'NO'
        row = col.row(align=True)
        row.scale_y=1.5
        prop = row.operator("view3d.hp_boolean_live", text="Subtract")
        prop.bool_operation = 'DIFFERENCE'
        prop.cutline = 'NO'
        prop.insetted = 'NO'
        prop.live = 'NO'
        prop.laser = 'NO'
        row = col.row(align=True)
        row.scale_y=1.5
        row.operator("view3d.hp_boolean_slice", text="Slice")

        prop = row.operator("view3d.hp_boolean_live", text="Wrap")
        prop.bool_operation = 'WRAP'
        prop.live = 'NO'
        prop.cutline = 'NO'
        prop.laser = 'NO'
        prop.insetted = 'NO'
        row = col.row(align=True)
        row.scale_y=1.5

        #Live Booleans
        split = pie.split()
        col = split.column(align=True)

        row = col.row(align=True)
        row.scale_y=1.5
        prop = row.operator("view3d.hp_boolean_live", text="Live Add")
        prop.bool_operation = 'UNION'
        prop.live = 'YES'
        prop.cutline = 'NO'
        prop.insetted = 'NO'
        prop.laser = 'NO'
        row = col.row(align=True)
        row.scale_y=1.5
        prop = row.operator("view3d.hp_boolean_live", text="Live Intersect")
        prop.bool_operation = 'INTERSECT'
        prop.cutline = 'NO'
        prop.insetted = 'NO'
        prop.live = 'YES'
        prop.laser = 'NO'
        row = col.row(align=True)
        row.scale_y=1.5
        prop = row.operator("view3d.hp_boolean_live", text="Live Subtract")
        prop.bool_operation = 'DIFFERENCE'
        prop.live = 'YES'
        prop.cutline = 'NO'
        prop.insetted = 'NO'
        prop.laser = 'NO'
        row = col.row(align=True)
        row.scale_y=1.5
        prop = row.operator("view3d.hp_boolean_live", text="Live Subtract Inset")
        prop.bool_operation = 'DIFFERENCE'
        prop.live = 'YES'
        prop.cutline = 'NO'
        prop.laser = 'NO'
        prop.insetted = 'YES'
        row = col.row(align=True)
        row.scale_y=1.5

        prop = row.operator("view3d.hp_boolean_live", text="Live Wrap")
        prop.bool_operation = 'WRAP'
        prop.live = 'YES'
        prop.cutline = 'NO'
        prop.laser = 'NO'
        prop.insetted = 'NO'
        row = col.row(align=True)
        row.scale_y=1.5

        prop = row.operator("view3d.hp_boolean_live", text="Live Cutline")
        prop.bool_operation = 'DIFFERENCE'
        prop.live = 'YES'
        prop.cutline = 'YES'
        prop.laser = 'NO'
        prop.insetted = 'NO'
        prop = row.operator("view3d.hp_boolean_live", text="Live Laser")
        prop.bool_operation = 'DIFFERENCE'
        prop.live = 'YES'
        prop.laser = 'YES'
        prop.insetted = 'NO'
        split = pie.split()
        col = split.column(align=True)

        row = col.row(align=True)
        row.scale_y=1.5
        row.operator("view3d.hp_boolean_apply", text="Apply Booleans and Copy").dup = 'YES'
        row = col.row(align=True)
        row.scale_y=1.5
        row.operator("view3d.hp_boolean_apply", text="Apply Booleans").dup = 'NO'
        row = col.row(align=True)
        row.scale_y=1.5
        row.operator("view3d.hp_boolean_apply", text="Apply All Modifiers").all = 'YES'
        #row.operator("view3d.hp_boolean_toggle_bool_solver", text="Toggle Solver")
        pie.operator("view3d.hp_boolean_toggle_cutters", text="Toggle Cutters")



class HP_OT_boolean_toggle_cutters(bpy.types.Operator):
    bl_idname = "view3d.hp_boolean_toggle_cutters"
    bl_label = "hp_boolean_toggle_cutters"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        for o in bpy.data.collections['Cutters'].objects:
            if o.hide_get() == False:
                o.hide_set(True)

            else:
                o.hide_set(False)
        return {'FINISHED'}
#class HP_Boolean_Toggle_Solver(bpy.types.Operator):
#    bl_idname = "view3d.hp_boolean_toggle_bool_solver"
#    bl_label = "hp_boolean_toggle_cutters"
#    bl_options = {'REGISTER', 'UNDO'}
#    def execute(self, context):
#        sel = bpy.context.selected_objects
#        view_layer = bpy.context.view_layer
#        bases = [base for base in view_layer.objects if not base.name.startswith("Bool_Cutter") and base.type == 'MESH']
#        for ob in sel:
#            #Get Cutters in Sel
#            if ob.name.startswith('Bool_Cutter'):
#                cutter = ob
#                for base in bases:
#                    for mod in base.modifiers:
#                        if mod.name == cutter.name:
#                            if mod.solver == 'BMESH':
#                                mod.solver = 'CARVE'
#                            else:
#                                mod.solver = 'BMESH'
#            else:
#                base = ob
#                for mod in base.modifiers:
#                    if mod.name.startswith ('Bool_Cutter'):
#                        if mod.solver == 'BMESH':
#                            mod.solver = 'CARVE'
#                        else:
#                            mod.solver = 'BMESH'
#        return {'FINISHED'}
class HP_OT_boolean_live(bpy.types.Operator):
    bl_idname = "view3d.hp_boolean_live"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    cutline: bpy.props.StringProperty(name='Cutline',default='NO')
    laser: bpy.props.StringProperty(name='Laser',default='NO')
    live: bpy.props.StringProperty(name='Live',default='NO')
    insetted: bpy.props.StringProperty(name='Insetted',default='NO')
    displaytype: bpy.props.StringProperty(name="Display Type",default='WIRE')
    showbounds: bpy.props.BoolProperty(name="Display Type",default= False)
    bool_operation: bpy.props.StringProperty(name="Boolean Operation")
    bool_solver: bpy.props.StringProperty(name="Boolean Solver",default='BMESH')
    def execute(self, context):
        sel = bpy.context.selected_objects
        base = bpy.context.active_object
        view_layer = bpy.context.view_layer
        isedit = False

        if bpy.context.active_object.mode != 'OBJECT' and self.live == 'NO':
            if self.bool_operation != 'WRAP':
                bpy.ops.mesh.select_linked(delimit={'NORMAL'})
                bpy.ops.mesh.intersect_boolean(operation=self.bool_operation)
                return {'FINISHED'}
        def create_cutter(displaytype, insetted, showbounds):
            bpy.context.view_layer.objects.active = cutter
            if self.bool_operation == 'WRAP':
                cutter.name = str(base.name + "_Wrap")
                Bool = cutter.modifiers.new(cutter.name, "BOOLEAN")
                Bool.object = base
                Bool.operation = 'INTERSECT'
                bpy.ops.object.modifier_add(type='DISPLACE')
                cutter.modifiers["Displace"].strength = 0.02
                bpy.ops.view3d.smart_shade_smooth_toggle('INVOKE_DEFAULT')
                bpy.context.view_layer.objects.active = base
            else:
                cutter.name = str(base.name + "_Cutter")
                view_layer_cutters = [obj for obj in view_layer.objects if "_Cutter" in obj.name]
                cutter.name = str(base.name + "_Cutter_" + str(len(view_layer_cutters)))
                for cut in cutter.modifiers:
                    if "_Cutter" in cut.name:
                       bpy.ops.object.modifier_apply(modifier=cut.name)
                if self.cutline == 'YES':
                    cutter.modifiers.new('Cutline', "SOLIDIFY")
                    bpy.context.object.modifiers['Cutline'].thickness = 0.02
                if self.laser == 'YES':
                    cutter.modifiers.new('Laser', "SOLIDIFY")
                    bpy.context.object.modifiers['Laser'].thickness = 100
                    bpy.context.object.modifiers['Laser'].offset = 0
                    bpy.context.object.show_all_edges = True
                if self.insetted == 'YES':
                    base.select_set(state=False)
                    cutter.select_set(state=True)
                    cutter.name = str(base.name + "_Inset_Cutter")
                    for x in view_layer_cutters:
                        bpy.ops.object.modifier_apply(modifier = x.name)
                    bpy.ops.object.duplicate()
                    bpy.context.view_layer.objects.active.name = str(base.name + "_Inset")
                    inset = bpy.context.active_object
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
                    bpy.ops.transform.resize(value=(0.92, 0.92, 0.92), constraint_axis=(False, False, False))
                    bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
                    bpy.ops.object.editmode_toggle()
                    bpy.context.view_layer.objects.active = cutter
                    bpy.ops.object.constraint_add(type='COPY_TRANSFORMS')
                    bpy.context.object.constraints["Copy Transforms"].target = inset
                    inset.select_set(state=True)
                    bpy.context.view_layer.objects.active = inset
                cutter.display_type = self.displaytype
                cutter.show_bounds = self.showbounds
                cutter.cycles_visibility.camera = False
                cutter.cycles_visibility.transmission = False
                cutter.cycles_visibility.diffuse = False
                cutter.cycles_visibility.scatter = False
                cutter.cycles_visibility.glossy = False
                cutter.cycles_visibility.shadow = False
                cutter.select_set(state=False)

        def create_bool(bool_operation, live):
            if self.bool_operation == 'WRAP':
                if self.live == 'NO':
                    bpy.ops.object.convert(target='MESH')
            else:
                Bool = base.modifiers.new(cutter.name, "BOOLEAN")
                Bool.object = cutter
                Bool.operation = bool_operation

                mirror = False
                if len([m for m in base.modifiers if m.name == "Mirror Base"]) > 0:
                    print('Base Mirrored')
                    mirror = True


                #Bool.solver = bool_solver
                base.select_set(state=True)
                bpy.context.view_layer.objects.active = base
                if mirror:
                    print('moving cutter up')
                    bpy.ops.object.modifier_move_up(modifier=cutter.name)
                # for o in bpy.context.selected_objects:
                    # bpy.context.view_layer.objects.active = o
                    # if 0 == len([m for m in bpy.context.object.modifiers if m.type == "SUBSURF"]):
                        # bpy.ops.object.modifier_move_down(modifier="Mirror Base")
                if self.live == 'NO':
                    if context.active_object.mode != 'OBJECT':
                        bpy.ops.object.editmode_toggle()
                    bpy.ops.object.modifier_apply(modifier=cutter.name)
                    base.select_set(state=False)
                    cutter.select_set(state=True)
                    bpy.ops.object.delete(use_global=False)
                    base.select_set(state=True)
                    i = base.data.vertex_colors.active_index
                    base.data.vertex_colors.active_index = i + 1
                    bpy.ops.mesh.vertex_color_remove()

        if context.active_object.mode != 'OBJECT':
            isedit = True
            bpy.ops.mesh.select_linked()
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.mesh.separate(type='SELECTED')
            bpy.ops.object.editmode_toggle()
            sel = bpy.context.selected_objects
        for cutter in sel:
            if cutter != base:
                create_cutter(self.displaytype, self.insetted, self.showbounds)
                create_bool(self.bool_operation, self.live)
        if isedit == True and self.live == 'NO':
            bpy.ops.object.editmode_toggle()
        if self.insetted == 'YES':
            base.select_set(state=False)
            for x in bpy.context.selected_objects:
                bpy.context.view_layer.objects.active = x

        try:
            bpy.data.collections['Cutters']
        except:
            print('Creating Cutters Collection')
            Cutcol = bpy.data.collections.new("Cutters")
            bpy.context.scene.collection.children.link(Cutcol)
        cutters = [obj for obj in bpy.data.objects if "_Cutter" in obj.name]
        for cutter in cutters:
            try:
                try:
                    bpy.context.scene.collection.objects.unlink(cutter)
                except:
                    for c in bpy.data.collections:
                        try:
                            c.objects.unlink(cutter)
                        except:
                            pass
                bpy.data.collections['Cutters'].objects.link(cutter)
            except:
                pass
        #bpy.ops.view3d.smart_shade_smooth_toggle('INVOKE_DEFAULT')
        return {'FINISHED'}
class HP_OT_boolean_slice(bpy.types.Operator):
    """slice"""
    bl_idname = "view3d.hp_boolean_slice"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    def invoke(self, context, event):
        if bpy.context.mode=='OBJECT':
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.object.vertex_group_add()
            bpy.ops.object.vertex_group_assign()
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.join()
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.vertex_group_select()
            bpy.ops.mesh.select_all(action='INVERT')
            bpy.ops.object.vertex_group_remove()
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
        bpy.ops.mesh.select_linked(delimit=set())
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.vertex_group_add()
        bpy.ops.object.vertex_group_assign()
        bpy.ops.mesh.intersect()
        bpy.ops.object.vertex_group_add()
        bpy.ops.object.vertex_group_assign()
        i = bpy.context.active_object.vertex_groups.active_index
        i = i-1
        bpy.context.active_object.vertex_groups.active_index = i
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.mesh.select_linked(delimit=set())
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.object.vertex_group_remove()
        bpy.ops.object.vertex_group_select()
        bpy.ops.object.vertex_group_remove()
        return {'FINISHED'}

class HP_OT_boolean_apply(bpy.types.Operator):
    bl_idname = "view3d.hp_boolean_apply"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    dup: bpy.props.StringProperty(name='Duplicate', default='NO')
    all: bpy.props.StringProperty(name='All Modifiers', default='NO')
    def execute(self, context):
        def apply(dup, all):
            sel = bpy.context.selected_objects
            view_layer = bpy.context.view_layer
            view_layer_cutters = [obj for obj in view_layer.objects if "_Cutter" in obj.name]
            base_cutters = []
            for ob in sel:
                if "_Cutter" in ob.name:
                    iscutter = True
                    cutter = ob
                    for base in view_layer.objects:
                        for mod in base.modifiers:
                            bpy.context.view_layer.objects.active = base
                            bpy.ops.object.modifier_apply(modifier=cutter.name)
                    cutter.select_set(state=True)
                else:
                    base = ob
                    if self.dup == 'YES':
                        bpy.ops.object.duplicate()
                        clone = bpy.context.active_object
                        base.hide_render = True

                    for mod in base.modifiers:
                        if self.all == 'YES':
                            bpy.ops.object.modifier_apply(modifier=mod.name)
                        try:
                            cutter = bpy.context.view_layer.objects[mod.name]
                            bpy.ops.object.modifier_apply(modifier=cutter.name)
                            if self.dup == 'YES':
                                # cutter.hide_render = True
                                continue
                            cutter.select_set(state=True)
                            base.select_set(state=False)
                            bpy.ops.object.delete()
                            base.select_set(state=True)
                        except:
                            pass

            try:
                if iscutter == True:
                    bpy.ops.object.delete()
                    bpy.context.active_object.select_set(state=True)
                    sel = bpy.context.selected_objects
            except:
                pass
        apply(self.dup, self.all)
        return {'FINISHED'}

classes = (
    HP_MT_pie_boolean,
    HP_OT_boolean_toggle_cutters,
    HP_OT_boolean_live,
    HP_OT_boolean_slice,
    HP_OT_boolean_apply,
)
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
