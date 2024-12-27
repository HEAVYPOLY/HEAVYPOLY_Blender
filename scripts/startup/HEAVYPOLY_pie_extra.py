
bl_info = {
    "name": "Pie Extra",
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
from bpy.types import Operator
from bpy.props import BoolProperty
from mathutils import Matrix
from bpy.props import StringProperty

class HP_MT_pie_extra(Menu):
    bl_label = "Extra"
    def draw(self, context):
        layout = self.layout
        view = context.space_data
        obj = context.active_object
        pie = layout.menu_pie()
        # Left
        pie.separator()
        

        # Right
        pie.separator()


        # Bottom
        pie.operator("object.origin_set_to_bottom", text="Origin -> Bottom", icon='TRIA_DOWN')


        # Top

        
        # Top Left
            
        

        
        # Top Right
        
        
        # Bottom Left
        

        # Bottom Right
            

        
   
class HP_OT_set_origin_to_bottom(Operator):
    bl_idname = "object.origin_set_to_bottom"
    bl_label = "Origin To Bottom"
    bl_description = "Set the Object Origin to the lowest point of each selected object"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if not any(
            [ob.type in {'MESH', 'ARMATURE'} for ob in context.selected_objects]
        ):
            cls.poll_message_set("No mesh or armature objects selected.")
            return False
        return True

    def execute(self, context):
        org_active_obj = context.active_object

        counter = 0
        for obj in context.selected_objects:
            counter += int(self.origin_to_bottom(context, obj))

        context.view_layer.objects.active = org_active_obj
        self.report(
            {'INFO'}, f"Moved the origins of {counter} objects to their lowest point."
        )

        return {'FINISHED'}

    @staticmethod
    def origin_to_bottom(context, obj) -> bool:
        if obj.type not in {'MESH', 'ARMATURE'}:
            return False

        org_mode = obj.mode

        try:
            if obj.type == 'MESH':
                bpy.ops.object.mode_set(mode='OBJECT')
                min_z = min([v.co.z for v in obj.data.vertices])
            elif obj.type == 'ARMATURE':
                context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                min_z = min(
                    [min([bone.head.z, bone.tail.z]) for bone in obj.data.edit_bones]
                )
            else:
                return False
        except ValueError:
            # min([]) would result in this error, so if the object is empty.
            return False

        if obj.type == 'MESH':
            for vert in obj.data.vertices:
                vert.co.z -= min_z
        elif obj.type == 'ARMATURE':
            for bone in obj.data.edit_bones:
                bone.head.z -= min_z
                bone.tail.z -= min_z

        obj.location.z += min_z

        bpy.ops.object.mode_set(mode=org_mode)
        return True
        
classes = (
    HP_MT_pie_extra,
    HP_OT_set_origin_to_bottom,
)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
