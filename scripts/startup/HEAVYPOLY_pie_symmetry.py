bl_info = {
    "name": "Pie Symmetry",
    "description": "Symmetry and Mirroring",
    "author": "Vaughan Ling",
    "blender": (2, 80, 0),
    "category": "Pie Menu"
    }

import bpy
from bpy.types import Menu

# symmetrize, mirror and mirror modifier

class HP_MT_pie_symmetry(Menu):
    bl_label = "Symmetry"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # left
        pie.operator("mesh.symmetrize_select_all", text="X").direction = 'POSITIVE_X'
        # right
        pie.operator("mesh.symmetrize_select_all", text="X").direction = 'NEGATIVE_X'
        # bottom
        pie.operator("mesh.symmetrize_select_all", text="Z").direction = 'POSITIVE_Z'
        # top
        pie.operator("mesh.symmetrize_select_all", text="Z").direction = 'NEGATIVE_Z'
        # topleft
        pie.operator("mesh.symmetrize_select_all", text="Y").direction = 'NEGATIVE_Y'
        # topright
        pie.operator("view3d.mirror_toggle", text="Live Mirror").type = 'Mirror Base'
        pie.operator("view3d.mirror_toggle", text="Live Mirror Local").type = 'Mirror Local'
        # bottomleft

#       split = pie.split()
#       col = split.column()
#       col.prop(bpy.context.object.modifiers['Mirror Base'], "use_clip", text="Clip at Center")
        pie.operator('view3d.mirror_clip_toggle', text='Center Clipping')
#       col.prop(bpy.context.object.modifiers['Mirror Base'], "mirror_object", text="")

        # bottomright
#       pie.operator("mesh.symmetrize_select_all", text="Y").direction = 'POSITIVE_Y'





class HP_OT_symmetrize_select_all(bpy.types.Operator):
    bl_idname = "mesh.symmetrize_select_all"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    direction: bpy.props.StringProperty(name="Direction")
    def invoke(self, context, event):
        def mirrorObjectmode(direction,event):
            # bpy.ops.object.mode_set(mode='EDIT')
            # bpy.ops.mesh.select_all(action='SELECT')
            # bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_inner=True, xstart=0, xend=1, ystart=1, yend=1)
            # bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.duplicate_move_linked()
            bpy.ops.transform.resize(value=(-1, 1, 1), constraint_axis=(True, False, False))

        def mirrorEditmode(direction, event):
            bpy.ops.object.mode_set(mode='EDIT')
            mesh = bpy.context.object.data
            totface = mesh.total_face_sel
            totedge = mesh.total_edge_sel
            totvert = mesh.total_vert_sel
            if event.ctrl:
                print('mirror selected elements')
                bpy.ops.mesh.symmetrize(direction=self.direction)
                return {'FINISHED'}
            bpy.ops.object.vertex_group_add()
            bpy.ops.object.vertex_group_assign()
            mirrorchildexists = False
            selob = bpy.context.object
            # if event.ctrl:
                # print('ctrl is held')
                # bpy.ops.mesh.select_linked(delimit={'SEAM'})
                # bpy.ops.object.separate_and_select()
                # bpy.ops.mesh.select_all(action='DESELECT')
                # bpy.ops.object.vertex_group_select()
                # bpy.ops.view3d.snap_cursor_to_selected()
                # bpy.ops.object.mode_set(mode='OBJECT')
                # bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                # print('origin set..')
                # bpy.ops.object.mode_set(mode='EDIT')
                # for m in bpy.context.object.modifiers:
                    # if m.name == "Mirror Child":
                        # mirrorchildexists = True
                # if mirrorchildexists == False:
                    # bpy.ops.object.modifier_remove(modifier="Mirror Base")
                    # bpy.context.object.modifiers.new("Mirror Child", "MIRROR")
                    # bpy.context.object.modifiers["Mirror Child"].mirror_object = selob
            bpy.ops.mesh.select_all(action='SELECT')            
            bpy.ops.mesh.symmetrize(direction=self.direction)
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.vertex_group_select()
            bpy.ops.object.vertex_group_remove(all=False, all_unlocked=False)
        if context.active_object.mode == 'OBJECT':
            print('mirror object mode')
            mirrorObjectmode(self.direction, event)
        elif context.active_object.mode == 'EDIT':
            print('mirror all elements')
            mirrorEditmode(self.direction, event)
        return {'FINISHED'}


        
class HP_OT_mirror_clip_toggle(bpy.types.Operator):
    bl_idname = "view3d.mirror_clip_toggle"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        for m in bpy.context.object.modifiers: 
            if m.type == 'MIRROR':      
                if m.use_clip == False:
                    m.use_clip = True
                else:
                    m.use_clip = False
        return {'FINISHED'}

class HP_OT_reset_center(bpy.types.Operator):
    bl_idname = "view3d.reset_center"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        if bpy.context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=False, scale=True)
            bpy.ops.object.mode_set(mode='EDIT')

        else:
            bpy.ops.object.transform_apply(location=True, rotation=False, scale=True)
        return {'FINISHED'}     

class HP_OT_mirror_toggle(bpy.types.Operator):
    bl_idname = "view3d.mirror_toggle"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    type: bpy.props.StringProperty(name='Type',default='Mirror Base') 
    def execute(self, event):
        def create_mirror(self, type):
            obmode = bpy.context.object.mode
            selobs = bpy.context.selected_objects
            
            if self.type == 'Mirror Base':
                obslist = [i.name for i in bpy.data.objects]
                if all(i != 'Mirror Origin' for i in obslist):
                    if bpy.context.object.mode == 'EDIT':
                        bpy.ops.object.mode_set(mode='OBJECT')
                        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
                        bpy.context.object.name = "Mirror Origin"
                        bpy.context.object.select_set(state=False)
                    else:
                        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
                        bpy.context.object.name = "Mirror Origin"
                        bpy.context.object.select_set(state=False)
            if len([a for a in selobs if a.name.startswith("Bool_Cutter")]) > 0:
                print ('Cutters Selected')
                for o in selobs:
                    o.select_set(state=False)
                    if o.name.startswith("Bool_Cutter"):
                        o.select_set(state=True)
            else:     
                print ('No Cutters Selected')
                for o in selobs:    
                    o.select_set(state=True)
            bpy.context.view_layer.objects.active = o
                          
            bpy.ops.object.mode_set(mode=obmode)
            o.modifiers.new(self.type, "MIRROR")
            if self.type == 'Mirror Base':
                bpy.context.object.modifiers[self.type].mirror_object = bpy.data.objects["Mirror Origin"]
                print('Creating Mirror Origin')
            bpy.context.object.modifiers[self.type].show_viewport = True
            bpy.context.object.modifiers[self.type].show_render = True
            #bpy.context.object.modifiers[self.type].use_clip = False
            bpy.context.object.modifiers[self.type].show_in_editmode = True
            #bpy.context.object.modifiers[self.type].use_bisect_axis[0] = True
            #bpy.context.object.modifiers[self.type].use_bisect_flip_axis[0] = True
            print('Setting Mirror Visible')
            #bpy.context.object.modifiers[self.type].show_on_cage = True
            if self.type == 'Mirror Local':
                print('Creating Mirror Local')
                bpy.ops.object.modifier_move_up(modifier=self.type)
        def mirror_visibility(self, type):      
            if len([m for m in bpy.context.object.modifiers if m.name == "Mirror Base"]) == 0:
                create_mirror(self,type)
            else:
                for m in bpy.context.object.modifiers: 
                    if m.name == self.type:
                        if m.show_viewport == True:
                            print('Hide Mirror')
                            m.show_viewport = False
                            m.show_render = False
                            m.show_in_editmode = False
                            #m.show_on_cage = False
                        else:
                            print('Show Mirror')
                            m.show_viewport = True
                            m.show_render = True
                            m.show_in_editmode = True
                            #m.show_on_cage = True
        
        obs = bpy.context.selected_objects
        for o in obs:
            #If there is no Mirror Base
            if 0 == len([m for m in bpy.context.object.modifiers if m.name == self.type]):
                create_mirror(self,type)
            else:
                mirror_visibility(self,type)
        return {'FINISHED'}
            



            
classes = (
    HP_MT_pie_symmetry,
    HP_OT_mirror_clip_toggle,
    HP_OT_mirror_toggle,
    HP_OT_symmetrize_select_all,
    HP_OT_reset_center
)
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register() 