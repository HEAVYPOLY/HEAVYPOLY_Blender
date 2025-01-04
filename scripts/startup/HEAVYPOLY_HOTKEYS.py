bl_info = {
    "name": "Heavypoly Hotkeys",
    "description": "Hotkeys",
    "author": "Vaughan Ling",
    "version": (0, 2, 0),
    "blender": (4, 3, 0),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "category": "Hotkeys"
    }

import bpy
import os

def kmi_props_setattr(kmi_props, attr, value):
    try:
        setattr(kmi_props, attr, value)
    except AttributeError:
        print("Warning: property '%s' not found in keymap item '%s'" %
              (attr, kmi_props.__class__.__name__))
    except Exception as e:
        print("Warning: %r" % e)

def Keymap_Heavypoly():

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    k_viewfit = 'MIDDLEMOUSE'
    k_manip = 'LEFTMOUSE'
    k_cursor = 'RIGHTMOUSE'
    k_nav = 'MIDDLEMOUSE'
    k_menu = 'SPACE'
    k_select = 'LEFTMOUSE'


    def Global_Keys():

        kmi = km.keymap_items.new("screen.userpref_show","TAB","PRESS", ctrl=True)
        # kmi = km.keymap_items.new("view3d.smart_scale","S","PRESS")
        kmi = km.keymap_items.new("wm.window_fullscreen_toggle","F11","PRESS")
        kmi = km.keymap_items.new('screen.animation_play', 'PERIOD', 'PRESS')
        #kmi = km.keymap_items.new("view3d.hp_duplicate_move","D","PRESS", shift=True)
#        kmi = km.keymap_items.new("wm.call_menu_pie","SPACE","PRESS", shift=True).properties.name='HP_MT_popup_uber'
#        kmi = km.keymap_items.new("wm.call_menu_pie","Z","PRESS").properties.name='HP_MT_popup_uber'
        kmi = km.keymap_items.new("popup.hp_properties", 'V',"PRESS", ctrl=True, shift=True)
        kmi = km.keymap_items.new("popup.hp_materials", 'V',"PRESS", shift=True)
    # kmi = km.keymap_items.new('gpencil.blank_frame_add', 'B', 'PRESS', key_modifier='FOUR')
# "ACCENT_GRAVE"
#Window
    km = kc.keymaps.new('Window', space_type='EMPTY', region_type='WINDOW', modal=False)
    Global_Keys()
    kmi = km.keymap_items.new('object.hide_viewport', 'H', 'PRESS')
    kmi = km.keymap_items.new('wm.save_homefile', 'U', 'PRESS', ctrl=True)
    kmi = km.keymap_items.new('transform.translate', 'SPACE', 'PRESS')
    #kmi = km.keymap_items.new('object.modal_translate', 'SPACE', 'PRESS')

    kmi = km.keymap_items.new('view3d.smart_delete', 'X', 'PRESS')
    kmi = km.keymap_items.new('mesh.dissolve_mode', 'X', 'PRESS',ctrl=True)
#kmi = km.keymap_items.new('transform.resize', 'SPACE', 'PRESS', alt=True)
    kmi = km.keymap_items.new('transform.rotate', 'C', 'PRESS')
    kmi = km.keymap_items.new("wm.call_menu_pie", k_menu,"PRESS",ctrl=True ,shift=True, alt=True).properties.name="HP_MT_pie_areas"
    kmi = km.keymap_items.new("wm.call_menu_pie", 'TAB',"PRESS",shift=True).properties.name="HP_MT_pie_areas"
    kmi = km.keymap_items.new("wm.revert_without_prompt","N","PRESS", alt=True)
    kmi = km.keymap_items.new("screen.redo_last","D","PRESS")
    kmi = km.keymap_items.new('wm.console_toggle', 'TAB', 'PRESS', ctrl=True, shift=True)

    kmi = km.keymap_items.new("wm.call_menu_pie","S","PRESS", ctrl=True).properties.name="HP_MT_pie_save"
    kmi = km.keymap_items.new("wm.call_menu_pie","S","PRESS", ctrl=True, shift=True).properties.name="HP_MT_pie_importexport"
    kmi = km.keymap_items.new('script.reload', 'U', 'PRESS', shift=True)
    kmi = km.keymap_items.new("screen.repeat_last","THREE","PRESS", ctrl=True, shift=True)
    kmi = km.keymap_items.new("ed.undo","TWO","PRESS", ctrl=True, shift=True)
    kmi = km.keymap_items.new('screen.frame_jump', 'PERIOD', 'PRESS', shift=True)



# Map Image
    km = kc.keymaps.new('Image', space_type='IMAGE_EDITOR', region_type='WINDOW', modal=False)
    Global_Keys()
    kmi = km.keymap_items.new('image.view_all', k_viewfit, 'PRESS', ctrl=True, shift=True)
    kmi_props_setattr(kmi.properties, 'fit_view', True)
    kmi = km.keymap_items.new('image.view_pan', k_nav, 'PRESS', shift=True)
    kmi = km.keymap_items.new('image.view_zoom', k_nav, 'PRESS', ctrl=True)

# Map Node Editor
    km = kc.keymaps.new('Node Editor', space_type='NODE_EDITOR', region_type='WINDOW', modal=False)
    kmi = km.keymap_items.new('node.view_selected', k_viewfit, 'PRESS', ctrl=True, shift=True)
# Map View2D
    km = kc.keymaps.new('View2D', space_type='EMPTY', region_type='WINDOW', modal=False)

# Map Animation
    km = kc.keymaps.new('Animation', space_type='EMPTY', region_type='WINDOW', modal=False)
    kmi = km.keymap_items.new('anim.change_frame', k_nav, 'PRESS')
    kmi = km.keymap_items.new('anim.change_frame', k_select, 'PRESS', alt = True)
    kmi = km.keymap_items.new('action.select_box', 'LEFTMOUSE', 'CLICK_DRAG', shift=True)
    kmi_props_setattr(kmi.properties, 'mode', 'ADD')
    kmi = km.keymap_items.new('action.select_box', 'LEFTMOUSE', 'CLICK_DRAG', ctrl=True)
    kmi_props_setattr(kmi.properties, 'mode', 'SUB')
    kmi = km.keymap_items.new('action.select_box', 'LEFTMOUSE', 'CLICK_DRAG')
    kmi_props_setattr(kmi.properties, 'mode', 'SET')
# Map DOPESHEET_EDITOR
    km = kc.keymaps.new('Dopesheet', space_type='DOPESHEET_EDITOR', region_type='WINDOW', modal=False)
    Global_Keys()
    #Dopesheet transform fix
    kmi = km.keymap_items.new('transform.transform', 'SPACE', 'PRESS', repeat=True)
    kmi.properties.mode = 'TIME_TRANSLATE'
    print(f"Created keymap: {km.name}")
    print(f"Added keymap item: {kmi.idname} ({kmi.type})")


    kmi = km.keymap_items.new('time.cursor_set', k_select, 'PRESS', alt = True)
    kmi = km.keymap_items.new('time.start_frame_set', 'S', 'PRESS')
    kmi = km.keymap_items.new('time.end_frame_set', 'E', 'PRESS')
    kmi = km.keymap_items.new('time.view_all', k_viewfit, 'PRESS', ctrl=True, shift=True)

# Map Graph Editor
    km = kc.keymaps.new('Graph Editor', space_type='GRAPH_EDITOR', region_type='WINDOW', modal=False)
    Global_Keys()
    kmi = km.keymap_items.new('graph.view_selected', k_viewfit, 'PRESS', ctrl=True, shift=True)
    kmi = km.keymap_items.new('graph.cursor_set', k_select, 'PRESS', alt = True)
    kmi = km.keymap_items.new('graph.select_box', 'LEFTMOUSE', 'CLICK_DRAG', shift=True)
    kmi_props_setattr(kmi.properties, 'mode', 'ADD')
    kmi = km.keymap_items.new('graph.select_box', 'LEFTMOUSE', 'CLICK_DRAG', ctrl=True)
    kmi_props_setattr(kmi.properties, 'mode', 'SUB')
    kmi = km.keymap_items.new('graph.select_box', 'LEFTMOUSE', 'CLICK_DRAG')
    kmi_props_setattr(kmi.properties, 'mode', 'SET')
# Map UV Editor
    km = kc.keymaps.new('UV Editor', space_type='EMPTY', region_type='WINDOW', modal=False)
    Global_Keys()
    kmi = km.keymap_items.new('image.view_selected', k_viewfit, 'PRESS', ctrl=True, shift=True)
    kmi = km.keymap_items.new("wm.call_menu_pie", k_menu,"PRESS",ctrl=True, alt=True).properties.name="HP_MT_pie_rotate90"
# Map Mask Editing
#    km = kc.keymaps.new('Mask Editing', space_type='EMPTY', region_type='WINDOW', modal=False)
#3D View
    km = kc.keymaps.new('3D View', space_type='VIEW_3D', region_type='WINDOW', modal=False)
    Global_Keys()
    kmi = km.keymap_items.new("view3d.smart_scale","S","PRESS")
    kmi = km.keymap_items.new("view3d.hp_draw","D","PRESS", ctrl=True)
#    kmi = km.keymap_items.new('view3d.render_border', 'B', 'PRESS', shift=True)
#    kmi = km.keymap_items.new('view3d.clear_render_border', 'B', 'PRESS', shift=True, ctrl=True)
    kmi = km.keymap_items.new('mesh.hp_extrude', 'SPACE', 'PRESS', shift=True)

    kmi = km.keymap_items.new('view3d.render_border', 'B', 'PRESS',shift=True, ctrl=True)
    kmi = km.keymap_items.new("wm.call_menu_pie", k_menu,"PRESS",ctrl=True ,shift=True, alt=True).properties.name="HP_MT_pie_areas"
    kmi = km.keymap_items.new('view3d.view_selected', k_nav, 'PRESS', ctrl=True, shift=True)
    kmi = km.keymap_items.new('view3d.move', k_nav, 'PRESS', shift=True)
    kmi = km.keymap_items.new('view3d.zoom', k_nav, 'PRESS', ctrl=True)
    kmi = km.keymap_items.new('view3d.rotate', k_nav, 'PRESS')
    kmi = km.keymap_items.new('view3d.manipulator', k_manip, 'PRESS')
    kmi = km.keymap_items.new("wm.call_menu_pie", k_menu,"PRESS",ctrl=True).properties.name="HP_MT_pie_select"
    kmi = km.keymap_items.new("wm.call_menu_pie", k_menu, 'PRESS',ctrl=True, alt=True).properties.name="HP_MT_pie_rotate90"
    kmi = km.keymap_items.new("wm.call_menu_pie", 'V', 'PRESS').properties.name="HP_MT_pie_view"
    kmi = km.keymap_items.new('wm.call_menu_pie', k_menu,'PRESS',ctrl=True, shift=True).properties.name="HP_MT_pie_pivots"
    kmi = km.keymap_items.new("wm.call_menu_pie","Z","PRESS").properties.name="HP_MT_pie_shading"
    kmi = km.keymap_items.new("wm.call_menu_pie","D","PRESS",ctrl=True, shift=True).properties.name="HP_MT_pie_specials"
    kmi = km.keymap_items.new("wm.call_menu_pie","ONE","PRESS").properties.name="HP_MT_pie_modifiers"
    kmi = km.keymap_items.new("wm.call_menu_pie","X","PRESS",shift=True).properties.name="HP_MT_pie_symmetry"
    kmi = km.keymap_items.new('wm.call_menu_pie', 'B', 'PRESS',ctrl=True).properties.name="HP_MT_pie_boolean"
    kmi = km.keymap_items.new("screen.repeat_last","Z","PRESS",ctrl=True, alt=True)
    kmi = km.keymap_items.new("screen.repeat_last","WHEELINMOUSE","PRESS",ctrl=True, shift=True, alt=True)
    kmi = km.keymap_items.new("ed.undo","WHEELOUTMOUSE","PRESS",ctrl=True, shift=True, alt=True)
    kmi = km.keymap_items.new("view3d.screencast_keys","U","PRESS",alt=True)
    kmi = km.keymap_items.new('view3d.select_lasso', 'LEFTMOUSE', 'CLICK_DRAG', shift=True, ctrl=True)
    kmi = km.keymap_items.new('view3d.select_box', 'LEFTMOUSE', 'CLICK_DRAG',ctrl=True).properties.mode='SUB'
    kmi = km.keymap_items.new('view3d.select_box', 'LEFTMOUSE', 'CLICK_DRAG',shift=True).properties.mode='ADD'
    kmi = km.keymap_items.new('view3d.select_box', 'LEFTMOUSE', 'CLICK_DRAG').properties.mode='SET'
    kmi = km.keymap_items.new("wm.search_menu","FIVE","PRESS")
    kmi = km.keymap_items.new("view3d.subdivision_toggle","TAB","PRESS")
    # kmi = km.keymap_items.new("view3d.smart_snap_cursor","RIGHTMOUSE","PRESS",ctrl=True)
    kmi = km.keymap_items.new("view3d.smart_snap_origin","RIGHTMOUSE","PRESS",ctrl=True, shift=True)
    kmi = km.keymap_items.new("view3d.smart_snap_cursor","RIGHTMOUSE","PRESS",ctrl=True)
    kmi = km.keymap_items.new("view3d.smart_snap_origin_collection","RIGHTMOUSE","PRESS",ctrl=True, shift=True, alt=True)


#Mesh
    km = kc.keymaps.new(name='Mesh')
    Global_Keys()
    # Double move operator
    #kmi = km.keymap_items.new("wm.modal_move_operator", 'SPACE', 'PRESS')
    #kmi = km.keymap_items.new('wm.toolbar', 'SPACE', 'PRESS')
    kmi = km.keymap_items.new('view3d.render_border', 'Z', 'PRESS', shift=True)
    # kmi = km.keymap_items.new('view3d.clear_render_border', 'Z', 'PRESS', shift=True, ctrl=True)
    kmi = km.keymap_items.new("mesh.dupli_extrude_cursor", 'E', 'PRESS')
    kmi = km.keymap_items.new("transform.edge_bevelweight", 'E', 'PRESS', ctrl=True, shift=True)
    #kmi = km.keymap_items.new('transform.translate', 'LEFTMOUSE', 'CLICK_DRAG')
    kmi = km.keymap_items.new('view3d.select_through_border', 'LEFTMOUSE', 'CLICK_DRAG')
    kmi = km.keymap_items.new('view3d.select_through_border_add', 'LEFTMOUSE', 'CLICK_DRAG',shift=True)
    kmi = km.keymap_items.new('view3d.select_through_border_sub', 'LEFTMOUSE', 'CLICK_DRAG',ctrl=True)
    kmi = km.keymap_items.new("wm.call_menu_pie","A","PRESS", shift=True).properties.name="HP_MT_pie_add"
    kmi = km.keymap_items.new("wm.call_menu","W","PRESS").properties.name="VIEW3D_MT_edit_mesh_context_menu"
    kmi = km.keymap_items.new("screen.userpref_show","TAB","PRESS", ctrl=True)
    kmi = km.keymap_items.new("view3d.subdivision_toggle","TAB","PRESS")
#    kmi = km.keymap_items.new('mesh.select_all', k_select, 'CLICK', ctrl=True)
#    kmi_props_setattr(kmi.properties, 'action', 'INVERT')
    kmi = km.keymap_items.new('mesh.shortest_path_pick', 'LEFTMOUSE', 'CLICK',ctrl=True, shift=True).properties.use_fill=True
    kmi = km.keymap_items.new('mesh.select_linked', k_select, 'DOUBLE_CLICK')
    kmi_props_setattr(kmi.properties, 'delimit', {'SEAM'})
    kmi = km.keymap_items.new('mesh.select_linked', k_select, 'DOUBLE_CLICK', shift=True)
    kmi_props_setattr(kmi.properties, 'delimit', {'SEAM'})
    kmi = km.keymap_items.new('mesh.select_more', 'WHEELINMOUSE', 'PRESS',ctrl=True, shift=True)
    kmi = km.keymap_items.new('mesh.select_less', 'WHEELOUTMOUSE', 'PRESS',ctrl=True, shift=True)
    kmi = km.keymap_items.new('mesh.select_more', 'Z', 'PRESS',alt=True)
    kmi = km.keymap_items.new('mesh.select_next_item', 'WHEELINMOUSE', 'PRESS', shift=True)
    kmi = km.keymap_items.new('mesh.select_next_item', 'Z', 'PRESS', shift=True)
    kmi = km.keymap_items.new('mesh.select_prev_item', 'WHEELOUTMOUSE', 'PRESS', shift=True)
    kmi = km.keymap_items.new('mesh.edgering_select', k_select, 'DOUBLE_CLICK', alt=True).properties.extend = False
    kmi = km.keymap_items.new('mesh.loop_multi_select', k_select, 'DOUBLE_CLICK', alt=True, shift=True)
    kmi = km.keymap_items.new('mesh.loop_select', k_select, 'PRESS', alt=True, shift=True).properties.extend = True
    kmi = km.keymap_items.new('mesh.loop_select', k_select, 'PRESS', alt=True).properties.extend = False
    kmi = km.keymap_items.new('mesh.normals_make_consistent', 'N', 'PRESS', ctrl=True).properties.inside = False
    kmi = km.keymap_items.new("wm.call_menu_pie","FOUR","PRESS").properties.name="GPENCIL_PIE_tool_palette"
    kmi = km.keymap_items.new("mesh.select_prev_item","TWO","PRESS")
    kmi = km.keymap_items.new("mesh.select_next_item","THREE","PRESS")
    kmi = km.keymap_items.new("mesh.select_less","TWO","PRESS", ctrl=True)
    kmi = km.keymap_items.new("mesh.select_more","THREE","PRESS", ctrl=True)
    kmi = km.keymap_items.new("mesh.inset", "SPACE", "PRESS", alt=True)
    kmi = km.keymap_items.new("mesh.push_and_slide","G","PRESS", shift=True)
#    kmi_props_setattr(kmi.properties, 'use_even_offset', True)
    kmi = km.keymap_items.new('object.separate_and_select', 'P', 'PRESS')
    kmi = km.keymap_items.new('mesh.bridge_edge_loops', 'B', 'PRESS', shift=True)
    kmi = km.keymap_items.new('mesh.bridge_edge_loops', 'B', 'PRESS', ctrl=True, shift=True).properties.number_cuts = 12
    kmi = km.keymap_items.new('transform.edge_bevelweight','B', 'PRESS', alt=True).properties.value = 1
    kmi = km.keymap_items.new('view3d.smart_bevel','B', 'PRESS')
    kmi = km.keymap_items.new('mesh.merge', 'J', 'PRESS', ctrl=True)
    kmi_props_setattr(kmi.properties, 'type', 'LAST')
    kmi = km.keymap_items.new('mesh.hp_unhide', 'H', 'PRESS', ctrl=True, shift=True)
#Grease Pencil
    km = kc.keymaps.new('Grease Pencil', space_type='EMPTY', region_type='WINDOW', modal=False)
    Global_Keys()
    kmi = km.keymap_items.new('gpencil.select_linked', k_select, 'DOUBLE_CLICK')
    kmi = km.keymap_items.new('gpencil.select_linked', k_select, 'DOUBLE_CLICK', shift=True)
    # kmi = km.keymap_items.new('gpencil.select_box', k_select,'CLICK_DRAG')
    # kmi_props_setattr(kmi.properties, 'mode', 'SET')
    # kmi_props_setattr(kmi.properties, 'wait_for_input',False)
    # kmi = km.keymap_items.new('gpencil.select_box', k_select,'CLICK_DRAG', ctrl=True)
    # kmi_props_setattr(kmi.properties, 'mode', 'SUB')
    # kmi_props_setattr(kmi.properties, 'wait_for_input',False)
    # kmi = km.keymap_items.new('gpencil.select_box', k_select, 'CLICK_DRAG', shift=True)
    # kmi_props_setattr(kmi.properties, 'mode', 'ADD')
    # kmi_props_setattr(kmi.properties, 'wait_for_input',False)
#Image Paint
    km = kc.keymaps.new(name='Image Paint')
    kmi = km.keymap_items.new('paint.sample_color', 'S', 'PRESS')
#Object Mode
    km = kc.keymaps.new(name='Object Mode')
    Global_Keys()
    # kmi = km.keymap_items.new('view3d.smart_bevel','B', 'PRESS')
    #kmi = km.keymap_items.new('object.select_all', k_select, 'CLICK_DRAG')
    #kmi_props_setattr(kmi.properties, 'action', 'DESELECT')
#    kmi = km.keymap_items.new('object.select_all', k_select, 'CLICK', ctrl=True)
#    kmi_props_setattr(kmi.properties, 'action', 'INVERT')
    kmi = km.keymap_items.new('object.hide_view_clear', 'H', 'PRESS', ctrl=True, shift=True)

#Sculpt Mode
    km = kc.keymaps.new(name='Sculpt')
    Global_Keys()
    kmi = km.keymap_items.new("wm.call_menu_pie", 'V', 'PRESS').properties.name="HP_MT_pie_view"

# Map Curve
    km = kc.keymaps.new('Curve', space_type='EMPTY', region_type='WINDOW', modal=False)
    Global_Keys()
    kmi = km.keymap_items.new('curve.select_linked', k_select, 'DOUBLE_CLICK', shift=True)
    kmi = km.keymap_items.new('curve.select_linked_pick', k_select, 'DOUBLE_CLICK')
    kmi = km.keymap_items.new('curve.reveal', 'H', 'PRESS', ctrl=True, shift=True)
    kmi = km.keymap_items.new('curve.shortest_path_pick', k_select, 'PRESS', ctrl=True, shift=True)
    kmi = km.keymap_items.new('curve.draw', 'LEFTMOUSE', 'PRESS', alt=True)

# Outliner
    km = kc.keymaps.new('Outliner', space_type='OUTLINER', region_type='WINDOW', modal=False)
    kmi = km.keymap_items.new('outliner.show_active', k_nav, 'PRESS', ctrl=True, shift=True)
    Global_Keys()

    kmi = km.keymap_items.new('wm.delete_without_prompt', 'X', 'PRESS')

# Lattice
    km = kc.keymaps.new(name='Lattice')
    Global_Keys()
    kmi = km.keymap_items.new('view3d.select_box', 'LEFTMOUSE', 'CLICK_DRAG', shift=False, ctrl=False)
    kmi = km.keymap_items.new('view3d.select_box', 'LEFTMOUSE', 'CLICK_DRAG', shift=True, ctrl=False)
    kmi_props_setattr(kmi.properties, 'mode', 'ADD')
    kmi = km.keymap_items.new('view3d.select_box', 'LEFTMOUSE', 'CLICK_DRAG', shift=False, ctrl=True)
    kmi_props_setattr(kmi.properties, 'mode', 'SUB')




#Function to disable keymap confict
def disable_default_kmi(km=None, idname=None, retries=1):
    wm = bpy.context.window_manager

    if not (km and idname) or retries < 1:
        return

    # the default keyconfig
    kc = wm.keyconfigs['Blender']
    for kmi in kc.keymaps[km].keymap_items:
        if kmi.idname == idname:
            kmi.active = False
            print("Disabled", kmi.name)
            return

    # add some delay
    bpy.app.timers.register(
        lambda: disable_default_kmi(km, idname,retries - 1),
        first_interval=0.1)
    
def disable_specific_kmi(km=None, idname=None, type=None, value=None, shift=None, ctrl=None, alt=None,  retries=1):
    wm = bpy.context.window_manager
    if not (km and idname) or retries < 1:
        return
    # the default keyconfig
    kc = wm.keyconfigs['Blender']
    for kmi in kc.keymaps[km].keymap_items:
        if kmi.idname == idname and kmi.type == type and kmi.value == value and kmi.shift == shift and kmi.ctrl == ctrl and kmi.alt == alt:
            kmi.active = False
            print("Disabled", kmi.name)
            return

    # add some delay
    bpy.app.timers.register(
        lambda: disable_specific_kmi(km, idname, type, value, shift, ctrl, alt, retries - 1),
        first_interval=0.1)

def get_active_kmi(space: str, **kwargs) -> bpy.types.KeyMapItem:
    kc = bpy.context.window_manager.keyconfigs.active
    km = kc.keymaps.get(space)
    if km:
        for kmi in km.keymap_items:
            for key, val in kwargs.items():
                if getattr(kmi, key) != val and val is not None:
                    break
            else:
                return kmi




def register():
    Keymap_Heavypoly()
    disable_default_kmi('Object Mode', 'transform.resize')
    disable_specific_kmi('Object Mode', 'transform.translate','LEFTMOUSE','CLICK_DRAG',False,False,False)
    disable_default_kmi('Object Mode', 'object.delete')
    disable_default_kmi('Object Mode', 'screen.animation_play')

    disable_specific_kmi('Curve', 'transform.translate','LEFTMOUSE','CLICK_DRAG',False,False,False)
    disable_specific_kmi('Curves', 'transform.translate','LEFTMOUSE','CLICK_DRAG',False,False,False)
    disable_specific_kmi('Curves', 'transform.translate','LEFTMOUSE','CLICK_DRAG',False,False,False)
    disable_specific_kmi('Grease Pencil Edit Mode', 'wm.call_menu','X','PRESS',False,False,False)



    disable_default_kmi('Object Mode', 'object.delete')

    disable_default_kmi('Window', 'screen.animation_play')

    disable_default_kmi('Frames', 'screen.animation_play')

    disable_default_kmi('Mesh', 'wm.call_menu')

    disable_specific_kmi('Sculpt', 'paint.brush_select','V','PRESS',False,False,False)
    
    disable_specific_kmi('3D View Tool: Select Box', 'view3d.select_box','LEFTMOUSE','CLICK_DRAG',False,False,False)
    disable_specific_kmi('3D View Tool: Select Box', 'view3d.select_box','LEFTMOUSE','CLICK_DRAG',True,False,False)
    disable_specific_kmi('3D View Tool: Select Box', 'view3d.select_box','LEFTMOUSE','CLICK_DRAG',False,True,False)
    disable_specific_kmi('3D View Tool: Select Box', 'view3d.select_box','LEFTMOUSE','CLICK_DRAG',True,True,False)
    
    
    kmi = get_active_kmi("3D View Tool: Move",
                         idname="transform.translate",
                         type='LEFTMOUSE',
                         value='CLICK_DRAG',
                         shift=False,
                         ctrl=False,
                         alt=False)
    kmi.active = False
    kmi = get_active_kmi("Pose",
                         idname="transform.translate",
                         type='LEFTMOUSE',
                         value='CLICK_DRAG',
                         shift=False,
                         ctrl=False,
                         alt=False)
    kmi.active = False
    kmi = get_active_kmi("Mesh",
                         idname="wm.call_menu",
                         type='X',
                         shift=False,
                         ctrl=False,
                         alt=False)
    kmi.active = False
    kmi = get_active_kmi("Grease Pencil Edit Mode",
                         idname="wm.call_menu",
                         type='X',
                         shift=False,
                         ctrl=False,
                         alt=False)
    print ("Disable GP Edit X")
    kmi.active = False
    kmi = get_active_kmi("Frames",
                         idname="screen.animation_play",
                         type='SPACE',
                         shift=True,
                         ctrl=True,
                         alt=False)
    kmi.active = False

        

    


def unregister():
    Keymap_Heavypoly()

if __name__ == "__main__":
    register()
