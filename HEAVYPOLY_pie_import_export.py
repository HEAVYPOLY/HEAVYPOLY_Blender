bl_info = {
    "name": "Pie Import Export",
    "description": "Import Export Pie",
    "author": "Vaughan Ling",
    "version": (0, 1, 0),
    "blender": (2, 79, 0),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "category": "Pie Menu"
    }

import bpy
from bpy.types import (
        Menu,
        Operator,
        )
import os

# save import export

class HP_MT_pie_importexport(Menu):
    bl_label = "Import Export"
    
    
    


    def draw(self, context):
        #L
        layout = self.layout
        pie = layout.menu_pie()
        box = pie.split().column()
        row = box.row(align=True)
        row.scale_y=1.5

        box.operator('wm.alembic_import', text='Import Alembic')
        box.operator('import_scene.fbx', text='Import FBX')
        box.operator('import_mesh.stl', text='Import STL')
        box.operator('import_scene.obj', text='Import OBJ')
        box.operator('import_image.to_plane', text='Import Image Plane')
        box.operator('wm.append', text = 'Append')
        box.operator("wm.link", text = "Link")
        #R
        box = pie.split().column()
        row = box.row(align=True)
        row.scale_y=1.5
        box.operator('wm.alembic_export', text='Export Alembic')
        box.operator('export_scene.fbx', text='Export FBX')
        box.operator('export_mesh.stl', text='Export STL')
        box.operator('export_scene.obj', text='Export OBJ')
        box.operator('image.save_as', text='Export Image')

        # bpy.ops.import_anim.bvh()
        # bpy.ops.import_scene.obj()
        # bpy.ops.import_curve.svg()
        # bpy.ops.import_image.to_plane()
#        bpy.ops.import_scene.autodesk_3ds()
#        bpy.ops.wm.collada_import()

#import_mesh.stl

        # box = pie.split().column()
        # row = box.row(align=True)

        # #9 - TOP - RIGHT
        # box = pie.split().column()
        # row = box.row(align=True)

def register():
    bpy.utils.register_class(HP_MT_pie_importexport)


def unregister():
    bpy.utils.unregister_class(HP_MT_pie_importexport)

if __name__ == "__main__":
    register()
