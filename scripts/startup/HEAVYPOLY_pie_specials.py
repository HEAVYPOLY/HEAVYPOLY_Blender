bl_info = {
    "name": "Pie Specials",
    "description": "Specials Modes",
    "author": "Vaughan Ling",
    "version": (0, 1, 0),
    "blender": (2, 78, 0),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "category": "Pie Menu"
    }

import bpy
import os
import mathutils
import numpy as np

from bpy.types import Menu
from bpy.types import Operator
from bpy.props import BoolProperty
from mathutils import Matrix
from bpy.props import StringProperty

# Path to the .blend file containing the node group
NODE_GROUP_FILE = os.path.join(os.path.dirname(__file__), "HP_Nodes.blend")

# Specials Pie
class HP_MT_pie_specials(Menu):
    bl_label = "Specials"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        # Load node groups dynamically
#Left
        prop=pie.operator("mesh.spin", text="Duplicate Radial")
        prop.dupli=True
        prop.angle=6.28319
#Right

#Bottom
        pie.operator("mesh.subdivide_cylinder", text='Subdivide Cylinder')
        pie.operator("object.origin_set_to_bottom", text="Origin to Bottom")
        


#Top
        split = pie.split()
        col = split.column(align=True)
        row = col.row(align=True)
        row.scale_y=1.5
        row.operator("object.quickpipe", text="Quick Pipe")
        row = col.row(align=True)
        row.operator("mesh.bridge_edge_loops", text = "Bridge Smooth").number_cuts=12
        row = col.row(align=True)
        row.scale_y=1.5
        
        pie.operator("view3d.hp_draw", text="Draw Primitives")

#TopLeft
        split = pie.split()
        col = split.column(align=True)
        row = col.row(align=True)
        row.scale_y=1.5
        row.operator("mesh.subdivide", text="Subdivide Smooth").smoothness=1
        row = col.row(align=True)
        row.scale_y=1.5
        row.operator("mesh.subdivide", text="Subdivide Flat").smoothness=0
        row = col.row(align=True)
        row.operator("transform.edge_crease", text="SUBD Crease ").value=1
        row.operator("transform.edge_crease", text="SUBD Un Crease").value=-1
        col.operator("object.scv_ot_draw_operator", text="Keys Viewer")
        col.operator("transform.vertex_random", text="Randomize")
        
        
#TopRight
        split = pie.split()
        col = split.column(align=True)
        row = col.row(align=True)
        row.scale_y=1.5
        row = col.row(align=True)
        row.operator("transform.tosphere", text="Make Round")
        row = col.row(align=True)
        row.operator("mesh.remove_doubles", text="Remove Doubles")
        #pie.operator("transform.tosphere", text="Make Round").value=1
        #pie.operator("mesh.remove_doubles", text="Remove Doubles")
        split = pie.split()
        col = split.column(align=True)
        row = col.row(align=True)
        row.scale_y=1.5
        row = col.row(align=True)
        row.operator("object.add_geo_nodes", text="Array Line").node_group_name = "HP_Array_Line"
        row = col.row(align=True)
        row.operator("object.add_geo_nodes", text="Array Circular").node_group_name = "HP_Array_Circle"
        row = col.row(align=True)
        row.operator("object.add_array_on_curve", text="Array on Curve")
        row = col.row(align=True)
        row.operator("object.add_scatter_on_faces", text="Scatter on Mesh")
        row = col.row(align=True)
        row.operator("object.add_geo_nodes", text="Displacement Noise").node_group_name = "HP_DisplaceNoise"
        row = col.row(align=True)
        row.operator("object.create_lattice_for_selection", text="Lattice")
        

        
#BottomLeft
        split = pie.split()

#BottomRight

class HP_OT_subdivide_cylinder(bpy.types.Operator):
    bl_idname = "mesh.subdivide_cylinder"        # unique identifier for buttons and menu items to reference.
    bl_label = "Subdivide Cylinder"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def execute(self, context):
        bpy.ops.mesh.loop_multi_select(ring=False)
        bpy.ops.mesh.loop_multi_select(ring=True)
        bpy.ops.mesh.bevel(offset_type='PERCENT', offset_pct=25, affect='EDGES')
        return {'FINISHED'}

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

###################################################################################
# ADD NODEGROUP TO THE MODIFIER
###################################################################################

# Ensure the specified node group exists in bpy.data.node_groups
def ensure_node_group_loaded(node_group_name):
    if node_group_name not in bpy.data.node_groups:
        with bpy.data.libraries.load(NODE_GROUP_FILE, link=False) as (data_from, data_to):
            if node_group_name in data_from.node_groups:
                data_to.node_groups = [node_group_name]
                print(f"Node group '{node_group_name}' loaded.")
    else:
        print(f"Node group '{node_group_name}' is already available.")

# Function to add a specific Geometry Nodes modifier to the selected object
def add_custom_geo_node(obj, node_group_name):
    ensure_node_group_loaded(node_group_name)
    
    if node_group_name not in bpy.data.node_groups:
        print(f"Node group '{node_group_name}' not found!")
        return
    
    # Add the Geometry Nodes modifier
    modifier = obj.modifiers.new(name=node_group_name, type='NODES')
    modifier.node_group = bpy.data.node_groups[node_group_name]
    print(f"Added Geometry Nodes modifier: {node_group_name}")


# Add a Geometry Nodes modifier to the curve and set the selected object as an input
def HP_Array_On_Curve(curve, obj, node_group_name):
    ensure_node_group_loaded(node_group_name)

    # Ensure the node group exists
    if node_group_name not in bpy.data.node_groups:
        print(f"Node group '{node_group_name}' not found!")
        return
    
    # Add the Geometry Nodes modifier to the curve
    modifier = curve.modifiers.new(name=node_group_name, type='NODES')
    modifier.node_group = bpy.data.node_groups[node_group_name]

    # Set the object as an input to the Geometry Node group
    modifier["Socket_3"]= obj
    print("Object attached to curve")

# Add a Geometry Nodes modifier to the curve and set the selected object as an input
def HP_Object_On_Faces(obj, obj2, node_group_name):
    ensure_node_group_loaded(node_group_name)

    # Ensure the node group exists
    if node_group_name not in bpy.data.node_groups:
        print(f"Node group '{node_group_name}' not found!")
        return
    
    # Add the Geometry Nodes modifier to the curve
    modifier = obj.modifiers.new(name=node_group_name, type='NODES')
    modifier.node_group = bpy.data.node_groups[node_group_name]

    # Set the object as an input to the Geometry Node group
    modifier["Socket_3"]= obj2
    print("Collection attached to Modifier")


# Operator to add the selected Geometry Nodes modifier
class HP_OBJECT_OT_add_geo_nodes(bpy.types.Operator):
    bl_idname = "object.add_geo_nodes"
    bl_label = "Add Specific Geometry Nodes"
    bl_description = "Add a specific Geometry Nodes modifier to the selected object"
    
    node_group_name: bpy.props.StringProperty()

    def execute(self, context):
        obj = context.object
        if obj and obj.type == 'MESH':  # Ensure the selected object is a mesh
            add_custom_geo_node(obj, self.node_group_name)
            self.report({'INFO'}, f"Added Geometry Nodes modifier: {self.node_group_name}")
        else:
            self.report({'WARNING'}, "Please select a mesh object.")
        return {'FINISHED'}

class HP_OBJECT_OT_add_Array_On_Curve(bpy.types.Operator):
    bl_idname = "object.add_array_on_curve"
    bl_label = "Assign Geometry Nodes to Curve"
    bl_description = "Assign a Geometry Nodes modifier to the selected curve, using the selected object as input"
    
    def execute(self, context):
        selected_objects = context.selected_objects
        if len(selected_objects) != 2:
            self.report({'WARNING'}, "Please select exactly one object and one curve.")
            return {'CANCELLED'}

        # Determine the curve and object
        obj1, obj2 = selected_objects
        curve = obj1 if obj1.type == 'CURVE' else obj2 if obj2.type == 'CURVE' else None
        obj = obj1 if obj1.type != 'CURVE' else obj2 if obj2.type != 'CURVE' else None

        if curve and obj:
            HP_Array_On_Curve(curve, obj, "HP_Array_On_Curve")  # Replace "NodeGroup1" with your node group name
            self.report({'INFO'}, f"Assigned Geometry Nodes modifier to {curve.name} with input {obj.name}")
        else:
            self.report({'WARNING'}, "Please select one curve and one object.")
            return {'CANCELLED'}

        return {'FINISHED'}
    #####################
class HP_OBJECT_OT_add_Scatter_On_Faces(bpy.types.Operator):
    bl_idname = "object.add_scatter_on_faces"
    bl_label = "Assign Geometry Nodes to Curve"
    bl_description = "Assign a Geometry Nodes modifier to the selected curve, using the selected object as input"
    
    def execute(self, context):
        selected_objects = context.selected_objects
        if len(selected_objects) != 2:
            self.report({'WARNING'}, "Please select exactly one object as base and one object to scatter.")
            return {'CANCELLED'}

        # Determine the curve and object
        obj_scatter, obj = selected_objects

        if obj_scatter and obj:
            # Create a vertex group with a specific name on the base object
            vertex_group_name = "Scattering_Mask"
            if vertex_group_name not in obj.vertex_groups:
                obj.vertex_groups.new(name=vertex_group_name)
                self.report({'INFO'}, f"Vertex group '{vertex_group_name}' created on {obj.name}.")
            else:
                self.report({'INFO'}, f"Vertex group '{vertex_group_name}' already exists on {obj.name}.")
            HP_Object_On_Faces(obj, obj_scatter, "HP_ScatterOnFaces") 
            self.report({'INFO'}, f"Assigned Geometry Nodes modifier to {obj.name} with input {obj_scatter.name}")
        else:
            self.report({'WARNING'}, "Please two objects")
            return {'CANCELLED'}

        return {'FINISHED'}
   
def findSelectedObjectsBBoxWithRotation(objs):
    """
    Calculate the oriented bounding box for multiple objects,
    taking into account their average rotation.
    """
    bbox_min = mathutils.Vector((float('inf'), float('inf'), float('inf')))
    bbox_max = mathutils.Vector((float('-inf'), float('-inf'), float('-inf')))
    
    # Sum of rotation matrices
    rotation_sum = mathutils.Matrix.Identity(3)
    object_count = len(objs)

    for ob in objs:
        for corner in ob.bound_box:
            # Transform corner to world coordinates
            world_corner = ob.matrix_world @ mathutils.Vector(corner)
            bbox_min.x = min(bbox_min.x, world_corner.x)
            bbox_min.y = min(bbox_min.y, world_corner.y)
            bbox_min.z = min(bbox_min.z, world_corner.z)
            bbox_max.x = max(bbox_max.x, world_corner.x)
            bbox_max.y = max(bbox_max.y, world_corner.y)
            bbox_max.z = max(bbox_max.z, world_corner.z)
        
        # Add object's rotation to the sum
        rotation_sum += ob.matrix_world.to_3x3()

    # Scale the summed matrix to get the average rotation
    avg_rotation = rotation_sum * (1.0 / object_count)

    # Convert average rotation to 4x4 for transformations
    avg_rotation_4x4 = avg_rotation.to_4x4()

    # Calculate the middle and scale of the bounding box
    middle = (bbox_max + bbox_min) / 2
    scale = (bbox_max - bbox_min)

    return middle, scale, avg_rotation_4x4


def create_lattice_for_selected_objects(context, divisions=(3, 3, 3), interp="KEY_BSPLINE"):
    # Calculate bounding box with average rotation
    middle, scale, avg_rotation = findSelectedObjectsBBoxWithRotation(context.selected_objects)

    # Create the lattice
    lattice = createLatticeObject(
        context,
        loc=middle,
        scale=scale,
        rot=avg_rotation.to_euler(),
        divisions=divisions,
        interp=interp
    )

    # Add lattice modifiers to all selected objects
    for obj in context.selected_objects:
        if obj.type == 'MESH':
            lattice_modifier = obj.modifiers.new(name="Lattice", type='LATTICE')
            lattice_modifier.object = lattice

    print(f"Lattice created for {len(context.selected_objects)} objects.")
    return lattice


def createLatticeObject(context, loc=mathutils.Vector((0.0, 0.0, 0.0)), scale=mathutils.Vector((1, 1, 1)),
                        rot=mathutils.Euler((0.0, 0.0, 0.0)), name=".latticetemp", 
                        divisions=[2, 2, 2], interp="KEY_BSPLINE", isoutside=True):
    # Create lattice data
    lat = bpy.data.lattices.new(name)
    ob = bpy.data.objects.new(name, lat)

    # Set lattice properties
    ob.data.use_outside = isoutside
    ob.data.points_u = divisions[0]
    ob.data.points_v = divisions[1]
    ob.data.points_w = divisions[2]

    ob.data.interpolation_type_u = interp
    ob.data.interpolation_type_v = interp
    ob.data.interpolation_type_w = interp

    # Link lattice to scene
    scene = context.scene
    scene.collection.objects.link(ob)

    # Set lattice location, scale, and rotation
    ob.location = loc
    ob.scale = scale
    ob.rotation_euler = rot

    return ob



class OBJECT_OT_create_lattice_for_selection(bpy.types.Operator):
    """Create a lattice for selected objects"""
    bl_idname = "object.create_lattice_for_selection"
    bl_label = "Create Lattice for Selection"
    bl_options = {'REGISTER', 'UNDO'}

    divisions: bpy.props.IntVectorProperty(
        name="Divisions",
        default=(3, 3, 3),
        size=3,
        min=2
    )
    interp: bpy.props.EnumProperty(
        name="Interpolation",
        items=[
            ('KEY_LINEAR', "Linear", ""),
            ('KEY_CARDINAL', "Cardinal", ""),
            ('KEY_BSPLINE', "B-Spline", "")
        ],
        default='KEY_BSPLINE'
    )

    def execute(self, context):
        create_lattice_for_selected_objects(context, divisions=self.divisions, interp=self.interp)
        return {'FINISHED'}





classes = (
    HP_MT_pie_specials,
    HP_OT_subdivide_cylinder,
    HP_OT_set_origin_to_bottom,
    HP_OBJECT_OT_add_geo_nodes,
    HP_OBJECT_OT_add_Array_On_Curve,
    OBJECT_OT_create_lattice_for_selection,
    HP_OBJECT_OT_add_Scatter_On_Faces,
)
register, unregister = bpy.utils.register_classes_factory(classes)


if __name__ == "__main__":
    register()