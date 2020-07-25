import bpy
from bpy.props import IntProperty, FloatProperty

bl_info = {
    "name": "Quick Pipe",
    "author": "floatvoid (Jeremy Mitchell)", "Vaughan Ling (2.8 conversion)"
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Edit Mode",
    "description": "Quickly converts an edge selection to an extruded curve.",
    "warning": "",
    "wiki_url": "",
    "category": "View3D"}


class jmPipeTool(bpy.types.Operator):
    """Create an extruded curve from a selection of edges"""
    bl_idname = "object.quickpipe"
    bl_label = "Quick Pipe"

    first_mouse_x: IntProperty()
    first_value: FloatProperty()
#   : bpy.props.StringProperty(name='Duplicate')
    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            delta = self.first_mouse_x - event.mouse_x
            context.object.data.bevel_depth = self.first_value + delta * 0.01
        elif event.type == 'WHEELUPMOUSE':
            bpy.context.object.data.bevel_resolution += 1
        elif event.type == 'WHEELDOWNMOUSE':
            if bpy.context.object.data.bevel_resolution > 0:
                bpy.context.object.data.bevel_resolution -= 1
        elif event.type == 'LEFTMOUSE':
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):

        if context.object:
            self.first_mouse_x = event.mouse_x
            if context.object.type == 'MESH':
                bpy.ops.mesh.duplicate_move()
                bpy.ops.object.separate_and_select()
                bpy.ops.object.editmode_toggle()
                # for mod in context.object.modifiers:
                    # bpy.ops.object.modifier_apply(apply_as='DATA')
                bpy.ops.object.convert(target='CURVE')
                self.pipe = bpy.context.view_layer.objects.active           
                self.pipe.data.fill_mode = 'FULL'
                self.pipe.data.splines[0].use_smooth = True
                self.pipe.data.bevel_resolution = 6
                self.pipe.data.bevel_depth = 0.1
            elif context.object.type == 'CURVE' :
                self.pipe = context.object
                        
            self.first_value = self.pipe.data.bevel_depth

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}



classes = (
    jmPipeTool,
)
register, unregister = bpy.utils.register_classes_factory(classes)  
    
if __name__ == "__main__":
    register() 