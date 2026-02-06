bl_info = {
    "name": "Pie Add",
    "description": "",
    "author": "Vaughan Ling (modified)",
    "version": (0, 1, 1),
    "blender": (2, 80, 0),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "category": "Pie Menu"
}

import bpy
import bmesh
from bpy.types import Menu, Operator
from bpy.props import StringProperty


def get_selected_face_material(obj):
    """Return the material datablock from the active face (or first selected face) in Edit Mode."""
    if not obj or obj.type != 'MESH':
        return None
    if bpy.context.mode != 'EDIT_MESH':
        return None

    bm = bmesh.from_edit_mesh(obj.data)
    face = bm.faces.active
    if face is None:
        sel = [f for f in bm.faces if f.select]
        face = sel[0] if sel else None

    if face is None:
        return None

    idx = face.material_index
    if 0 <= idx < len(obj.material_slots):
        return obj.material_slots[idx].material
    return None


def apply_single_material(obj, mat):
    """Make obj use exactly one material slot: mat (index 0)."""
    if not obj or obj.type != 'MESH' or mat is None:
        return
    # Clear then append so join can match by datablock and reuse existing slots.
    obj.data.materials.clear()
    obj.data.materials.append(mat)


class HP_MT_pie_add(Menu):
    bl_label = "Add"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # Left
        split = pie.split()
        col = split.column()
        col.scale_y = 1.5
        col.scale_x = 1.1
        col.operator("view3d.hp_add_primitive", icon='MESH_PLANE', text="Big").type = 'Plane'
        col.operator("view3d.hp_add_primitive", icon='MESH_PLANE', text="Small").type = 'Plane_Small'
        col.operator("view3d.hp_add_primitive", icon='MESH_CUBE', text="Big").type = 'Cube'
        col.operator("view3d.hp_add_primitive", icon='MESH_CUBE', text="Small").type = 'Cube_Small'

        col = split.column()
        col.scale_y = 1.5
        col.scale_x = 1
        col.operator("view3d.hp_add_primitive", icon='MESH_CIRCLE', text="6").type = 'Circle_6'
        col.operator("view3d.hp_add_primitive", icon='MESH_CIRCLE', text="8").type = 'Circle_8'
        col.operator("view3d.hp_add_primitive", icon='MESH_CIRCLE', text="12").type = 'Circle_12'
        col.operator("view3d.hp_add_primitive", icon='MESH_CIRCLE', text="24").type = 'Circle_24'
        col.operator("view3d.hp_add_primitive", icon='MESH_CIRCLE', text="32").type = 'Circle_32'

        # Right
        split = pie.split()
        col = split.column()
        col.scale_y = 1.5
        col.scale_x = 1
        col.operator("view3d.hp_add_primitive", icon='MESH_UVSPHERE', text="12").type = 'Sphere_12'
        col.operator("view3d.hp_add_primitive", icon='MESH_UVSPHERE', text="24").type = 'Sphere_24'
        col.operator("view3d.hp_add_primitive", icon='MESH_UVSPHERE', text="32").type = 'Sphere_32'

        # Top
        split = pie.split()
        col = split.column()
        col.scale_y = 1.5
        col.scale_x = 1
        col.operator("view3d.hp_add_primitive", icon='IPO_EASE_IN_OUT', text="Curve").type = 'Curve'
        col.operator("view3d.hp_add_primitive", icon='CURVE_NCIRCLE', text="Curve").type = 'Curve Circle'

        col = split.column()
        col.scale_y = 1.5
        col.scale_x = 1
        col.operator("view3d.hp_add_primitive", icon='LIGHT', text="Light").type = 'Point_Light'
        col.operator("view3d.hp_add_primitive", icon='LIGHT_AREA', text="Light").type = 'Area_Light'
        col.operator("view3d.hp_add_primitive", icon='GREASEPENCIL', text="GPencil").type = 'Grease_Pencil'

        # Bottom
        split = pie.split()
        col = split.column()
        col.scale_y = 1.5
        col.scale_x = 1
        col.operator("view3d.hp_add_primitive", icon='MESH_CYLINDER', text="6").type = 'Cylinder_6'
        col.operator("view3d.hp_add_primitive", icon='MESH_CYLINDER', text="8").type = 'Cylinder_8'
        col.operator("view3d.hp_add_primitive", icon='MESH_CYLINDER', text="12").type = 'Cylinder_12'
        col.operator("view3d.hp_add_primitive", icon='MESH_CYLINDER', text="24").type = 'Cylinder_24'

        col = split.column()
        col.scale_y = 1.5
        col.scale_x = 1
        col.operator("view3d.hp_add_primitive", icon='MESH_CYLINDER', text="32").type = 'Cylinder_32'
        col.operator("view3d.hp_add_primitive", icon='MESH_CYLINDER', text="64").type = 'Cylinder_64'
        col.operator("view3d.hp_add_primitive", icon='MESH_CYLINDER', text="128").type = 'Cylinder_128'


class HP_OT_add_primitive(Operator):
    bl_idname = "view3d.hp_add_primitive"
    bl_label = "HP Add Primitive"
    bl_options = {'REGISTER', 'UNDO'}

    type: StringProperty(name="Type")

    def invoke(self, context, event):
        cur = context.scene.cursor.location.copy()
        addob = False

        # Determine align mode based on current 3D view
        align_mode = 'WORLD'
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        if space.region_3d.is_perspective:
                            align_mode = 'WORLD'
                        else:
                            align_mode = 'VIEW'
                        break

        def prim():
            t = self.type

            if t == 'Cube':
                bpy.ops.mesh.primitive_cube_add(size=1, align=align_mode)
            elif t == 'Cube_Small':
                bpy.ops.mesh.primitive_cube_add(size=.1, align=align_mode)
            elif t == 'Plane':
                bpy.ops.mesh.primitive_plane_add(align=align_mode)
            elif t == 'Plane_Small':
                bpy.ops.mesh.primitive_plane_add(size=.1, align=align_mode)

            elif t == 'Circle_6':
                bpy.ops.mesh.primitive_circle_add(vertices=6, radius=0.08, fill_type='NGON', align=align_mode)
            elif t == 'Circle_8':
                bpy.ops.mesh.primitive_circle_add(fill_type='NGON', radius=.25, vertices=8, align=align_mode)
            elif t == 'Circle_12':
                bpy.ops.mesh.primitive_circle_add(fill_type='NGON', radius=.25, vertices=12, align=align_mode)
            elif t == 'Circle_24':
                bpy.ops.mesh.primitive_circle_add(fill_type='NGON', radius=.25, vertices=24, align=align_mode)
            elif t == 'Circle_32':
                bpy.ops.mesh.primitive_circle_add(fill_type='NGON', vertices=32, align=align_mode)

            elif t == 'Cylinder_6':
                bpy.ops.mesh.primitive_cylinder_add(radius=.08, depth=.1, vertices=6, align=align_mode)
            elif t == 'Cylinder_8':
                bpy.ops.mesh.primitive_cylinder_add(radius=.25, depth=.5, vertices=8, align=align_mode)
            elif t == 'Cylinder_12':
                bpy.ops.mesh.primitive_cylinder_add(radius=.25, depth=.5, vertices=12, align=align_mode)
            elif t == 'Cylinder_24':
                bpy.ops.mesh.primitive_cylinder_add(radius=.25, depth=.5, vertices=24, enter_editmode=False, align=align_mode)
            elif t == 'Cylinder_32':
                bpy.ops.mesh.primitive_cylinder_add(vertices=32, align=align_mode)
            elif t == 'Cylinder_64':
                bpy.ops.mesh.primitive_cylinder_add(vertices=64, align=align_mode)
            elif t == 'Cylinder_128':
                bpy.ops.mesh.primitive_cylinder_add(vertices=128, align=align_mode)

            elif t == 'Sphere_12':
                bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.1, align=align_mode)
            elif t == 'Sphere_24':
                bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, align=align_mode)
            elif t == 'Sphere_32':
                bpy.ops.mesh.primitive_uv_sphere_add(align=align_mode)

            elif t == 'Grease_Pencil':
                bpy.ops.object.gpencil_add()
                bpy.ops.object.mode_set(mode='GPENCIL_PAINT')
            elif t == 'Curve':
                bpy.ops.curve.primitive_nurbs_path_add()
                bpy.ops.object.editmode_toggle()

            elif t == 'Point_Light':
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.light_add(type='POINT', radius=.05, align=align_mode)
                context.active_object.name = 'Light Point'
                context.object.data.energy = 200
                context.object.data.shadow_soft_size = 0.3
                context.object.data.shadow_buffer_bias = 0.1
                context.object.data.shadow_buffer_clip_start = 0.1

            elif t == 'Area_Light':
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.light_add(type='AREA', radius=1, align=align_mode)
                context.active_object.name = 'Light Area'
                context.active_object.data.shape = 'RECTANGLE'
                context.active_object.data.size = 1
                context.active_object.data.size_y = 3
                context.active_object.data.energy = 200
                context.active_object.data.shadow_soft_size = 0.3
                context.active_object.data.shadow_buffer_bias = 0.1
                context.active_object.data.shadow_buffer_clip_start = 0.1

        # Save current transform orientation
        t_axis = context.scene.transform_orientation_slots[0].type

        def create_aligned_to_faces():
            o = context.view_layer.objects.active

            # 1) Grab material from selected face BEFORE we leave edit mode / deselect
            target_mat = get_selected_face_material(o)

            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.ops.transform.create_orientation(name="AddAxis", use=True, overwrite=True)
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

            # 2) Create primitive (new object becomes active)
            prim()
            new_obj = context.view_layer.objects.active

            # 3) Force the primitive to use ONLY the target material (so join reuses the slot)
            if target_mat and new_obj and new_obj.type == 'MESH':
                apply_single_material(new_obj, target_mat)

            bpy.ops.transform.transform(mode='ALIGN', value=(0, 0, 0, 0))

            if addob is False:
                # Re-activate original mesh and join
                o.select_set(state=True)
                context.view_layer.objects.active = o
                bpy.ops.object.join()
                bpy.ops.object.mode_set(mode='EDIT')

        if self.type in {'Point_Light', 'Area_Light', 'Grease_Pencil'}:
            addob = True

        # If no selection at all
        if context.object and context.object.type == 'MESH' and context.object.data.total_vert_sel == 0:
            prim()

        # Face select mode
        elif tuple(context.scene.tool_settings.mesh_select_mode) == (False, False, True):
            create_aligned_to_faces()

        else:
            # Other selection modes: keep your original behavior
            bpy.ops.view3d.snap_cursor_to_selected()
            prim()

        # Restore cursor + transform orientation
        context.scene.cursor.location = cur
        bpy.data.scenes[0].transform_orientation_slots[0].type = t_axis

        return {'FINISHED'}


classes = (
    HP_MT_pie_add,
    HP_OT_add_primitive,
)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
