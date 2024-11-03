bl_info = {
    'name': 'Hannah_Hotkeys',
    'description': 'Hotkeys',
    'author': 'Hannah Ümit and Sas van Gulik',
    'version': (0, 1, 0),
    'blender': (4, 1, 0),
    'location': '',
    'warning': '',
    'wiki_url': '',
    'category': 'Hotkeys'
    }

import bpy

def get_keymap_items_ctx(window_manager, KeyMapConfig: str, keymap_context: str):
    return window_manager.keyconfigs[KeyMapConfig].keymaps[keymap_context].keymap_items

def add_keymap_attrs(keymap_items, 
                     idname: str, 
                     event_type: str, 
                     value_key, 
                     any=False, 
                     shift=0, 
                     ctrl=0, 
                     alt=0, 
                     oskey=0, 
                     key_modifier='NONE', 
                     direction='ANY', 
                     repeat=False, 
                     head=False,
                     **kwargs):

    keymap = keymap_items.new(idname,event_type,value_key,any=any,shift=shift,ctrl=ctrl,alt=alt,oskey=oskey,key_modifier=key_modifier,direction=direction,repeat=repeat,head=head)

    # https://blender.stackexchange.com/questions/195823/how-to-keymap-a-custom-operator-with-properties
    if not keymap.properties:
        raise ValueError
    keyw_args = {k : v for k, v in kwargs.items() if hasattr(keymap.properties, k)}
    for attr, val in keyw_args.items():
        setattr(keymap.properties, attr, val)

    return keymap

def Keymap_Hannah():
    
    def Global_Keys():
        keymap = add_keymap_attrs(km, 'screen.userpref_show', 'TAB', 'PRESS' , ctrl=True)
        keymap = add_keymap_attrs(km, 'wm.window_fullscreen_toggle','F11','PRESS')
        keymap = add_keymap_attrs(km, 'screen.animation_play', 'PERIOD', 'PRESS')

# Map Window
    km = get_keymap_items_ctx(bpy.context.window_manager,'Blender', 'Window')
    Global_Keys()
    keymap = add_keymap_attrs(km, 'object.hide_viewport', 'H', 'PRESS')
    keymap = add_keymap_attrs(km, 'wm.save_homefile', 'U', 'PRESS', ctrl=True)
    keymap = add_keymap_attrs(km, 'transform.translate', 'SPACE', 'PRESS')
    keymap = add_keymap_attrs(km, 'view3d.smart_delete', 'X', 'PRESS')
    keymap = add_keymap_attrs(km, 'mesh.dissolve_mode', 'X', 'PRESS',ctrl=True)
    keymap = add_keymap_attrs(km, 'wm.revert_without_prompt','N','PRESS', alt=True)
    keymap = add_keymap_attrs(km, 'screen.redo_last','D','PRESS')
    keymap = add_keymap_attrs(km, 'wm.console_toggle', 'TAB', 'PRESS', ctrl=True, shift=True)
    keymap = add_keymap_attrs(km, 'wm.call_menu_pie','S','PRESS', ctrl=True, name='HP_MT_pie_save')
    keymap = add_keymap_attrs(km, 'wm.call_menu_pie','S','PRESS', ctrl=True, shift=True, name='HP_MT_pie_importexport')
    keymap = add_keymap_attrs(km, 'script.reload', 'U', 'PRESS', shift=True)

# Map Image
    km = get_keymap_items_ctx(bpy.context.window_manager,'Blender', 'Image')
    Global_Keys()
    keymap = add_keymap_attrs(km, 'image.view_all', 'MIDDLEMOUSE', 'PRESS', ctrl=True, shift=True, fit_view=True)
    keymap = add_keymap_attrs(km, 'image.view_pan', 'MIDDLEMOUSE', 'PRESS', shift=True)
    keymap = add_keymap_attrs(km, 'image.view_zoom', 'MIDDLEMOUSE', 'PRESS', ctrl=True)

# Map Node Editor
    km = get_keymap_items_ctx(bpy.context.window_manager,'Blender', 'Node Editor')
    Global_Keys()
    keymap = add_keymap_attrs(km, 'node.view_selected', 'MIDDLEMOUSE', 'PRESS', ctrl=True, shift=True)
    
# Map View2D
    km = get_keymap_items_ctx(bpy.context.window_manager,'Blender', 'View2D')

# Map Animation
    km = get_keymap_items_ctx(bpy.context.window_manager,'Blender', 'Animation')
    Global_Keys()
    keymap = add_keymap_attrs(km, 'anim.change_frame', 'MIDDLEMOUSE', 'PRESS')
    keymap = add_keymap_attrs(km, 'action.select_box', 'LEFTMOUSE', 'CLICK_DRAG', shift=True, mode='ADD')
    keymap = add_keymap_attrs(km, 'action.select_box', 'LEFTMOUSE', 'CLICK_DRAG', ctrl=True, mode='SUB')
    keymap = add_keymap_attrs(km, 'action.select_box', 'LEFTMOUSE', 'CLICK_DRAG', mode='SET')
    keymap = add_keymap_attrs(km, 'anim.start_frame_set', 'S', 'PRESS')
    keymap = add_keymap_attrs(km, 'anim.end_frame_set', 'E', 'PRESS')
    
# Map Dopesheet
    km = get_keymap_items_ctx(bpy.context.window_manager,'Blender', 'Dopesheet')
    Global_Keys()
    keymap = add_keymap_attrs(km, 'transform.transform', 'SPACE', 'PRESS' , mode='TIME_TRANSLATE')
    keymap = add_keymap_attrs(km, 'clip.dopesheet_view_all  ', 'MIDDLEMOUSE', 'PRESS', ctrl=True, shift=True)

# Map Graph Editor
    km = get_keymap_items_ctx(bpy.context.window_manager,'Blender', 'Graph Editor')
    Global_Keys()
    keymap = add_keymap_attrs(km, 'graph.view_selected', 'MIDDLEMOUSE', 'PRESS', ctrl=True, shift=True)
    keymap = add_keymap_attrs(km, 'graph.cursor_set', 'LEFTMOUSE', 'PRESS', alt = True)
    keymap = add_keymap_attrs(km, 'graph.select_box', 'LEFTMOUSE', 'CLICK_DRAG', shift=True, mode='ADD')
    keymap = add_keymap_attrs(km, 'graph.select_box', 'LEFTMOUSE', 'CLICK_DRAG', ctrl=True, mode='SUB')
    keymap = add_keymap_attrs(km, 'graph.select_box', 'LEFTMOUSE', 'CLICK_DRAG', mode='SET')
    
# Map UV Editor
    km = get_keymap_items_ctx(bpy.context.window_manager,'Blender', 'UV Editor')
    Global_Keys()
    keymap = add_keymap_attrs(km, 'image.view_selected', 'MIDDLEMOUSE', 'PRESS', ctrl=True, shift=True)
    
#Map 3D View
    km = get_keymap_items_ctx(bpy.context.window_manager,'Blender', '3D View')
    Global_Keys()
    keymap = add_keymap_attrs(km, 'mesh.hp_extrude', 'SPACE', 'PRESS', shift=True)
    keymap = add_keymap_attrs(km, 'view3d.render_border', 'B', 'PRESS',shift=True, ctrl=True)
    keymap = add_keymap_attrs(km, 'view3d.view_selected', 'MIDDLEMOUSE', 'PRESS', ctrl=True, shift=True)
    keymap = add_keymap_attrs(km, 'view3d.move', 'MIDDLEMOUSE', 'PRESS', shift=True)
    keymap = add_keymap_attrs(km, 'view3d.zoom', 'MIDDLEMOUSE', 'PRESS', ctrl=True)
    keymap = add_keymap_attrs(km, 'view3d.rotate', 'MIDDLEMOUSE', 'PRESS')
    keymap = add_keymap_attrs(km, 'view3d.manipulator', 'LEFTMOUSE', 'PRESS')
    keymap = add_keymap_attrs(km, 'wm.call_menu_pie', 'SPACE','PRESS',ctrl=True, name='HP_MT_pie_select')
    keymap = add_keymap_attrs(km, 'wm.call_menu_pie', 'SPACE', 'PRESS',ctrl=True, alt=True, name='HP_MT_pie_rotate90')
    keymap = add_keymap_attrs(km, 'wm.call_menu_pie', 'V', 'PRESS', name='HP_MT_pie_view')
    keymap = add_keymap_attrs(km, 'wm.call_menu_pie', 'SPACE','PRESS',ctrl=True, shift=True, name='HP_MT_pie_pivots')
    keymap = add_keymap_attrs(km, 'wm.call_menu_pie','Z','PRESS', name='HP_MT_pie_shading')
    keymap = add_keymap_attrs(km, 'wm.call_menu_pie', 'B', 'PRESS',ctrl=True, name='HP_MT_pie_boolean')
    keymap = add_keymap_attrs(km, 'screen.repeat_last','Z','PRESS',ctrl=True, alt=True)
    keymap = add_keymap_attrs(km, 'view3d.screencast_keys','U','PRESS',alt=True)
    keymap = add_keymap_attrs(km, 'view3d.select_lasso', 'LEFTMOUSE', 'CLICK_DRAG', shift=True, ctrl=True)
    keymap = add_keymap_attrs(km, 'view3d.select_box', 'LEFTMOUSE', 'CLICK_DRAG',ctrl=True, mode='SUB')
    keymap = add_keymap_attrs(km, 'view3d.select_box', 'LEFTMOUSE', 'CLICK_DRAG',shift=True, mode='ADD')
    keymap = add_keymap_attrs(km, 'view3d.select_box', 'LEFTMOUSE', 'CLICK_DRAG', mode='SET')
    keymap = add_keymap_attrs(km, 'view3d.subdivision_toggle','TAB','PRESS')
    
#Map Mesh
    km = get_keymap_items_ctx(bpy.context.window_manager,'Blender', 'Mesh')
    Global_Keys()
    keymap = add_keymap_attrs(km, 'view3d.render_border', 'Z', 'PRESS', shift=True)
    keymap = add_keymap_attrs(km, 'mesh.dupli_extrude_cursor', 'E', 'PRESS')
    keymap = add_keymap_attrs(km, 'transform.edge_bevelweight', 'E', 'PRESS', ctrl=True, shift=True)
    keymap = add_keymap_attrs(km, 'view3d.select_through_border', 'LEFTMOUSE', 'CLICK_DRAG')
    keymap = add_keymap_attrs(km, 'view3d.select_through_border_add', 'LEFTMOUSE', 'CLICK_DRAG',shift=True)
    keymap = add_keymap_attrs(km, 'view3d.select_through_border_sub', 'LEFTMOUSE', 'CLICK_DRAG',ctrl=True)
    keymap = add_keymap_attrs(km, 'wm.call_menu','W','PRESS', name='VIEW3D_MT_edit_mesh_context_menu')
    keymap = add_keymap_attrs(km, 'view3d.subdivision_toggle','TAB','PRESS')
    keymap = add_keymap_attrs(km, 'mesh.select_linked', 'LEFTMOUSE', 'DOUBLE_CLICK', delimit={'SEAM'})
    keymap = add_keymap_attrs(km, 'mesh.edgering_select', 'LEFTMOUSE', 'DOUBLE_CLICK', alt=True, extend=False)
    keymap = add_keymap_attrs(km, 'mesh.loop_multi_select', 'LEFTMOUSE', 'DOUBLE_CLICK', alt=True, shift=True)
    keymap = add_keymap_attrs(km, 'mesh.loop_select', 'LEFTMOUSE', 'PRESS', alt=True, shift=True, extend =True)
    keymap = add_keymap_attrs(km, 'mesh.loop_select', 'LEFTMOUSE', 'PRESS', alt=True, extend=False)
    keymap = add_keymap_attrs(km, 'mesh.normals_make_consistent', 'N', 'PRESS', ctrl=True, extend=False)
    keymap = add_keymap_attrs(km, 'mesh.select_prev_item','TWO','PRESS')
    keymap = add_keymap_attrs(km, 'mesh.select_next_item','THREE','PRESS')
    keymap = add_keymap_attrs(km, 'mesh.select_less','TWO','PRESS', ctrl=True)
    keymap = add_keymap_attrs(km, 'mesh.select_more','THREE','PRESS', ctrl=True)
    keymap = add_keymap_attrs(km, 'mesh.inset', 'SPACE', 'PRESS', alt=True)
    keymap = add_keymap_attrs(km, 'object.separate_and_select', 'P', 'PRESS')
    keymap = add_keymap_attrs(km, 'mesh.bridge_edge_loops', 'B', 'PRESS', shift=True)
    keymap = add_keymap_attrs(km, 'mesh.bridge_edge_loops', 'B', 'PRESS', ctrl=True, shift=True, number_cuts=12)
    keymap = add_keymap_attrs(km, 'transform.edge_bevelweight','B', 'PRESS', alt=True, value=1.0)
    keymap = add_keymap_attrs(km, 'mesh.bevel','B', 'PRESS')
    keymap = add_keymap_attrs(km, 'mesh.merge', 'J', 'PRESS', ctrl=True, type='LAST')
    keymap = add_keymap_attrs(km, 'mesh.hp_unhide', 'H', 'PRESS', ctrl=True, shift=True)

# Map Grease Pencil
    km = get_keymap_items_ctx(bpy.context.window_manager,'Blender',  'Grease Pencil')
    Global_Keys()
    keymap = add_keymap_attrs(km, 'gpencil.select_linked', 'LEFTMOUSE', 'DOUBLE_CLICK', shift=True)

# Map Image Paint
    km = get_keymap_items_ctx(bpy.context.window_manager,'Blender',  'Image Paint')
    Global_Keys()
    keymap = add_keymap_attrs(km, 'paint.sample_color', 'S', 'PRESS')

# Map Object Mode
    km = get_keymap_items_ctx(bpy.context.window_manager,'Blender',  'Object Mode')
    Global_Keys()
    keymap = add_keymap_attrs(km, 'object.hide_view_clear', 'H', 'PRESS', ctrl=True, shift=True)

# Map Curve
    km = get_keymap_items_ctx(bpy.context.window_manager,'Blender',  'Curve')
    Global_Keys()
    keymap = add_keymap_attrs(km, 'curve.select_linked', 'LEFTMOUSE', 'DOUBLE_CLICK', shift=True)
    keymap = add_keymap_attrs(km, 'curve.select_linked_pick', 'LEFTMOUSE', 'DOUBLE_CLICK')
    keymap = add_keymap_attrs(km, 'curve.reveal', 'H', 'PRESS', ctrl=True, shift=True)
    keymap = add_keymap_attrs(km, 'curve.shortest_path_pick', 'LEFTMOUSE', 'PRESS', ctrl=True, shift=True)
    keymap = add_keymap_attrs(km, 'curve.draw', 'LEFTMOUSE', 'PRESS', alt=True)

# Map Outliner
    km = get_keymap_items_ctx(bpy.context.window_manager,'Blender',  'Outliner')
    Global_Keys()
    keymap = add_keymap_attrs(km, 'outliner.show_active', 'MIDDLEMOUSE', 'PRESS', ctrl=True, shift=True)
    keymap = add_keymap_attrs(km, 'wm.delete_without_prompt', 'X', 'PRESS')



def register():
    Keymap_Hannah()

def unregister():
    Keymap_Hannah()

if __name__ == '__main__':
    register()
