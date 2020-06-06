bl_info = {
    "name": "HP Draw Primitives",
    "author": "Vaughan Ling",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    }
import bpy
import bgl
import blf
import bmesh
import time
import mathutils
import math
import random
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import intersect_line_plane
from bpy_extras.view3d_utils import (
    region_2d_to_vector_3d,
    region_2d_to_origin_3d)

def draw_callback_px(self, context):
    font_id = 0
    y = 60
    y_offset = 0
    lines = [
        'SPACE    | Finish',
        'C             | Color',
        'ALT         | Rotate',
        'S             | Shape = ' + self.shape.capitalize(),
        'CTRL B  | Show/Hide Cutters', 
        'X             | Live = ' + str(self.live),
        'B             | Cut Type = '+ str(self.bool),
        'SHIFT     | Extrude',
        ]
        
    blf.size(font_id, 20, 42)
    for l in lines:
        blf.position(font_id, 30, (y + y_offset), 0)
        blf.color(font_id,.02,.02,.02,1)
        blf.draw(font_id, l)
        y_offset += 30
    # if self.dragging:
        # if self.shape == 'circle':
            # blf.position(font_id, 300, 30, 0)
            # blf.draw(font_id, 'A / D = Resolution = ' + str(self.res*100) + '%')    

    blf.size(font_id, 20, 72)
    blf.position(font_id, 30, y_offset + 60, 0)
    blf.draw(font_id, 'DRAG  | Draw')
# class VIEW3D_PT_hp_draw(bpy.types.Panel):
    # bl_space_type = 'VIEW_3D'
    # bl_region_type = 'UI'
    # bl_category = "HP Draw"
    # bl_label = "HP Draw"
             

class HP_OT_draw_primitives(bpy.types.Operator):
    """Draw a line with the mouse"""
    bl_idname = "view3d.hp_draw"
    bl_label = "Draw Primitives"
    bl_space_type = "VIEW_3D"
    def invoke(self, context, event):
        if not bpy.context.object.type == 'MESH':
            self.report({'INFO'}, 'Selected Object is not a mesh')
            return {'FINISHED'}
        args = (self, context)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
        self.verts = []
        self.clicks = []
        self.click = False
        self.normal = None
        self.normal_saved = (1,0,1)
        self.hit_saved = (1,1,1)
        self.res = 1
        self.mouse_path_x = []
        self.mouse_path_y = []
        self.mesh_verts = None
        self.mouse_events = [('START')]
        self.dragging = False
        self.shifting = False
        self.first_hit = None
        self.first_mouse_x = event.mouse_x
        self.first_mouse_y = event.mouse_y
        self.first_mouse_res_x = event.mouse_x
        self.first_mouse_res_y = event.mouse_y
        self.solidify_value = 0.0
        self.offset = .001
        self.hit = None
        self.bool = 'None'
        self.shape_count = 0
        self.bool_count = 0
        self.hit_length = 0
        self.face_index = None
        self.originfound = False
        self.vector = None
        self.live = 'NO'
        self.shape = 'box'
        self.rotate = False
        self.normalsflipped = False
        self.initial_ob = bpy.context.active_object
        self.delta = 0
        self.mode = 'Draw'
        self.colormode = 'sat'
        self.hue = bpy.data.brushes["Draw"].color.h 
        self.value = bpy.data.brushes["Draw"].color.v
        context.window_manager.modal_handler_add(self)
        self.bvhtree = self.bvhtree_from_object(context, context.active_object)
        self.drawbox = None
        self.data_to_remove = []
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        try:
            def draw_vert(vertlist):
                #if vertlist empty
                if vertlist == []:
                    #if no previous hit
                    try:
                        #If Geo under mouse, get first hit
                        self.first_hit = self.get_mouse_3d_on_mesh(event, context)
                        print('Geo Under Mouse')
                        vertlist.append(self.first_hit)

                    except:
                        #If no geo under mouse, use previous hit
                        print('No Geo Under Mouse')
                        vertlist.append(self.get_mouse_3d_on_plane(event, context, self.hit_saved, self.normal_saved))
                        # print(self.normal)
                        # print(self.hit)
                        self.hit = self.hit_saved
                        self.normal = self.normal_saved
                else:
                    vertlist.append(self.get_mouse_3d_on_plane(event, context, self.hit, self.normal))

                if len(vertlist) > 2: 
                    self.create_mesh(self.create_mesh_verts(vertlist, self.shape))
            def finish_box():
                if len(bpy.context.object.data.vertices) != 0:
                    if len(bpy.context.object.modifiers) > 0:
                        bpy.ops.object.convert(target='MESH')
                    cur_ob = bpy.ops.object
                    # rvalue = random.random()
                    # bpy.ops.paint.vertex_paint_toggle()
                    # bpy.ops.paint.vertex_color_set()
                    #bpy.ops.paint.vertex_color_hsv(h=rvalue)
                    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                    self.initial_ob.select_set(state=True)
                    bpy.context.view_layer.objects.active = self.initial_ob
                    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
                    # bpy.obs.object.to_mesh_clear()
                    # bpy.ops.object.select_set(state=True)
                    if self.bool == 'None':
                        print(cur_ob.data)
                        bpy.ops.object.join()
                        # bpy.context.view_layer.update()
                                    
                        # self.data_to_remove.append(cur_ob.data)
                        # for block in bpy.data.meshes:
                            # if block.users == 0:
                                # print('removed ', block)
                                # bpy.data.meshes.remove(block)
                        # for block in bpy.data.materials:
                            # if block.users == 0:
                                # bpy.data.materials.remove(block)

                        # for block in bpy.data.textures:
                            # if block.users == 0:
                                # bpy.data.textures.remove(block)

                        # for block in bpy.data.images:
                            # if block.users == 0:
                                # bpy.data.images.remove(block)
                        # self.initial_ob.select_set(state=True)
                        # invoke(self, context, event)
                        bpy.context.view_layer.update()
                    if self.bool == 'Subtract':
                        bpy.ops.view3d.hp_boolean_live(live = self.live, bool_operation = 'DIFFERENCE')
                    if self.bool == 'Add':
                        bpy.ops.view3d.hp_boolean_live(live = self.live, bool_operation = 'UNION')
                    if self.bool == 'Wrap':
                        bpy.ops.view3d.hp_boolean_live(live = self.live, bool_operation = 'WRAP')
                    # bpy.ops.view3d.smart_shade_smooth_toggle('INVOKE_DEFAULT')
                else:
                    bpy.ops.view3d.smart_delete('INVOKE_DEFAULT')
                    self.initial_ob.select_set(state=True)
                    bpy.context.view_layer.objects.active = self.initial_ob
                self.verts = []
                self.hit_saved = self.hit
                self.normal_saved = self.normal
                
                self.originfound = False
                self.mode = 'Draw'
                self.click = False
                self.colormode = 'sat'
                # self.initial_ob.select_set(state=True)

                self.bvhtree = self.bvhtree_from_object(context, context.active_object)
                bpy.ops.ed.undo_push(message="Box Drawn")
                print('Box Drawn')
            context.area.tag_redraw()
            
            
            if event.type in {'RIGHTMOUSE', 'ESC', 'SPACE'}:
                if event.value == 'PRESS':

                    bpy.context.view_layer.update()
                    bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
                    return {'FINISHED'}
            
            if event.type == 'MOUSEMOVE':
                self.mouse_path_x.append(event.mouse_x)
                self.mouse_path_y.append(event.mouse_y)
            if event.ctrl:
                self.ctrl = True
            else:
                self.ctrl = False
            if event.shift:
                self.shift = True
            else:
                self.shift = False
            if event.type in {"MIDDLEMOUSE", "V", "Z","WHEELUPMOUSE", "WHEELDOWNMOUSE", "E", "SPACE"}:
                return {"PASS_THROUGH"}
            if event.value == 'PRESS':
                # if event.type == 'R':
                    # self.first_mouse_res_x = event.mouse_x
                    # self.first_mouse_res_y = event.mouse_y
                    # self.mode = 'Resolution'
                    
                if event.type in {'F', 'WHEELDOWNMOUSE'}:
                    if len(self.create_mesh_verts(self.verts[1], self.verts[-1], self.shape)) > 4:
                        self.res -= .05
                if event.type == 'E':
                    bpy.ops.ui.eyedropper_color('INVOKE_DEFAULT')
                if event.type == 'S':
                    shapetypes = ['box', 'circle', 'polyline']
                    if self.shape_count == len(shapetypes)-1:
                        self.shape_count = 0
                    else:
                        self.shape_count += 1
                    self.shape = shapetypes[self.shape_count]
                if event.type == 'B':
                    booltypes = ['None', 'Subtract', 'Add', 'Wrap']
                    if event.ctrl:
                        bpy.ops.view3d.hp_boolean_toggle_cutters('INVOKE_DEFAULT')
                        return {'RUNNING_MODAL'}
                    if self.bool_count == len(booltypes)-1:
                        self.bool_count = 0
                    else:
                        self.bool_count += 1
                    self.bool = booltypes[self.bool_count]
                if event.type == 'X':
                    if self.live == 'NO':
                        self.live = 'YES'
                    else:
                        self.live = 'NO'
                if event.type == 'LEFT_ALT':
                    self.mode = 'Rotate'
                    self.first_mouse_x = event.mouse_x
                    self.first_mouse_y = event.mouse_y
                if event.type == 'LEFT_SHIFT':
                    startmode = self.mode
                    self.first_mouse_x = event.mouse_x
                    self.first_mouse_y = event.mouse_y
                    self.mode = 'Thicken'
            if event.type == 'C':
                if self.dragging:
                    if event.value == 'PRESS':
                        self.startmode = self.mode
                        self.mode = 'Color'
                        self.first_mouse_x = event.mouse_x
                        self.first_mouse_y = event.mouse_y
                        if self.colormode == 'hue':
                            self.colormode = 'sat'
                        else:
                            self.colormode = 'hue'

            if event.type == 'LEFTMOUSE':
                if event.value == 'PRESS':
                    self.initial_ob = bpy.context.active_object
                    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                    
                    self.create_object()
                    print('press')
                    self.dragging = True
                    self.lastevent = time.time()
                if event.value == 'RELEASE':
                    # if time.time()-self.lastevent <.1:
                        # self.click = True
                        # print('First Click')
                    # if self.click:
                        # print('Click')
                    self.dragging = False
                    finish_box()
            if self.dragging:
                self.delta = (-(event.mouse_y - self.first_mouse_y) + (self.first_mouse_x - event.mouse_x)) * self.hit_length
                # print('dragging')
                if self.mode == 'Draw':
                    draw_vert(self.verts)                     
                if self.mode == 'Thicken':
                    self.thickness_delta = self.delta
                    if len(bpy.context.object.modifiers) == 0:
                        bpy.ops.object.modifier_add(type='SOLIDIFY')
                    if len(bpy.context.object.modifiers) > 0:
                        if self.axis == 'y':
                            bpy.context.object.modifiers["Solidify"].thickness = -self.thickness_delta * 0.002
                        else:
                            bpy.context.object.modifiers["Solidify"].thickness = self.thickness_delta * 0.002
                # if self.mode == 'Resolution':
                    # self.res == .5
                if self.mode == 'Rotate':
                    if self.originfound == False:
                        bpy.ops.view3d.smart_snap_origin('INVOKE_DEFAULT')
                        self.originfound = True
                    if self.axis == 'x':
                        bpy.context.object.rotation_euler[0] = self.delta * -0.0004
                    if self.axis == 'y':
                        bpy.context.object.rotation_euler[1] = self.delta * -0.0004
                    if self.axis == 'z':
                        bpy.context.object.rotation_euler[2] = self.delta * -0.0004

                #if bpy.context.object.mode != 'VERTEX_PAINT':
                if self.mode == 'Color':
                    bpy.ops.object.mode_set(mode='VERTEX_PAINT', toggle=False)
                    bpy.ops.paint.vertex_color_set()   

                        
                    color_delta_x = (self.mouse_path_x[-2]-self.mouse_path_x[-1])*-.001
                    color_delta_y = (self.mouse_path_y[-2]-self.mouse_path_y[-1])*-.001
                    if self.colormode == 'sat':
                        bpy.data.brushes["Draw"].color.s += color_delta_x
                    if self.colormode == 'hue':
                        bpy.data.brushes["Draw"].color.h += color_delta_x
                    bpy.data.brushes["Draw"].color.v += color_delta_y
                    bpy.ops.paint.vertex_color_set()
                    bpy.ops.object.mode_set(mode='OBJECT', toggle=False) 


            return {'RUNNING_MODAL'}

        except:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'FINISHED'}
    def create_mesh(self, verts):
        bm = bmesh.new()
        for v in verts:
            bm.verts.new(v)
        bm.faces.new(bm.verts)
        # bm.update()
        bm.to_mesh(bpy.context.object.data)
        bm.free()
        
        # self.new_face_normal = bpy.context.object.data.polygons[0].normal
        # if (abs(self.normal.x - self.new_face_normal.x)+abs(self.normal.y - self.new_face_normal.y)+abs(self.normal.z - self.new_face_normal.z)) > .1:
            # self.normalsflipped = not self.normalsflipped
        
        # bpy.ops.object.mode_set(mode='VERTEX_PAINT', toggle=False)
        # bpy.ops.paint.vertex_color_set()   
        # bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        
    def create_object(self):
        mesh = bpy.data.meshes.new("Draw_Box")
        self.draw_box = bpy.data.objects.new("Draw_Box", mesh)
        bpy.context.scene.collection.objects.link(self.draw_box)
        bpy.context.view_layer.objects.active = self.draw_box
        # bpy.context.view_layer.update()
        # bpy.context.object.active_material = bpy.data.materials['Diffuse_V']
        bpy.ops.object.select_all(action='DESELECT')
        self.draw_box.select_set(state=True)
        
    def create_mesh_verts(self, verts, shape):
        click1 = verts[0]
        click2 = verts[-1]
        if abs(click1.x - click2.x) < .01:
            self.axis = 'x'
        if abs(click1.y - click2.y) < .01:
            self.axis = 'y'
        if abs(click1.z - click2.z) < .01:
            self.axis = 'z'
        if shape == 'box':
            a = 0,0,0
            b = 0,0,0
            if self.axis == 'x':
                a = click1.x, click2.y, click1.z
                b = click1.x, click1.y, click2.z
            if self.axis == 'y':
                a = click1.x, click1.y, click2.z
                b = click2.x, click1.y, click1.z
            if self.axis == 'z':
                a = click1.x, click2.y, click1.z
                b = click2.x, click1.y, click1.z
            if self.normalsflipped:
                return (click1, b, click2, a)
            else:
                return (click1, a, click2, b)
        if shape == 'circle':
            pi = math.pi
            r = (abs(click1.x - click2.x) + abs(click1.y - click2.y) )
            self.n = int(3 + 64*r * self.res)
            if self.axis == 'x':
                circle = [(click1.x, click1.y + math.cos(2*pi/self.n*x)*r, click1.z + math.sin(2*pi/self.n*x)*r) for x in range(0,self.n+1)]
            elif self.axis == 'y':
                circle = [(click1.x + math.cos(2*pi/self.n*x)*r, click1.y, click1.z + math.sin(2*pi/self.n*x)*r) for x in range(0,self.n+1)]
            elif self.axis == 'z':
                circle = [(click1.x + math.cos(2*pi/self.n*x)*r, click1.y + math.sin(2*pi/self.n*x)*r,click1.z) for x in range(0,self.n+1)]
            if self.normalsflipped:
                return circle
            else:
                return circle
        if shape == 'polyline':
            return verts


        
        
    def bvhtree_from_object(self, context, object):
        # bm = bmesh.new()
        # mesh = object.to_mesh()
        # bm.from_mesh(mesh)
        # bm.transform(object.matrix_world)
        
        # bvhtree = BVHTree.FromBMesh(bm)
        
        
        # object.data.transform(object.matrix_world)

        # bpy.context.view_layer.depsgraph.update()
        # bm.free()

        # bvhtree = BVHTree.FromObject(object, bpy.context.view_layer.depsgraph )
        
        snapSurface = object
        context.view_layer.depsgraph.objects[snapSurface.name].data.transform(snapSurface.matrix_world)
        sourceSurface_BVHT = BVHTree.FromObject(snapSurface, context.view_layer.depsgraph)
        context.view_layer.depsgraph.objects[snapSurface.name].data.transform(snapSurface.matrix_world.inverted())
        return sourceSurface_BVHT

    def get_origin_and_direction(self, event, context):
        region    = context.region
        region_3d = context.space_data.region_3d
        mouse_coord = (event.mouse_region_x, event.mouse_region_y)
        origin    = region_2d_to_origin_3d(region, region_3d, mouse_coord)
        direction = region_2d_to_vector_3d(region, region_3d, mouse_coord)
        return origin, direction
        
    def get_mouse_3d_on_mesh(self, event, context):
        origin, direction = self.get_origin_and_direction(event, context)
        self.hit, self.normal, *_ = self.bvhtree.ray_cast(origin, direction, 1000)
        
        # print('Ray Cast ', self.bvhtree.ray_cast(origin, direction, 1000))
        if self.hit is not None:
            self.hit = self.hit + (self.normal * self.offset * random.random())
        self.hit_length = (origin - self.hit).length
        return self.hit

    def get_mouse_3d_on_plane(self, event, context, hit, normal):            
        origin, direction = self.get_origin_and_direction(event, context)
        return intersect_line_plane(origin, origin + direction, hit, normal, True)
             
def register():
    bpy.utils.register_class(HP_OT_draw_primitives)
    # bpy.utils.register_class(VIEW3D_PT_hp_draw)

def unregister():
    bpy.utils.unregister_class(HP_OT_draw_primitives)
    # bpy.utils.unregister_class(VIEW3D_PT_hp_draw)


if __name__ == "__main__":
    register()
