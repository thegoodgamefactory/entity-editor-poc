import dearpygui.dearpygui as dpg

def save_callback():
    print("Save Clicked")

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

dummy_attributes = [
    'attr_minimap_colour',
    'attr_handle_portal_collision',
    'attr_stage_1_arrow_bullets_collide'
]

dummy_components = { 
    'moves' : {},
    'position' : {},
    'speed': {'speed': 15},
    'velocity': {'x': 1, 'y': 0},
}

width, height, channels, data = dpg.load_image("slug.png")

with dpg.texture_registry():
    dpg.add_static_texture(width=width, height=height, default_value=data, tag="entity_texture")

with dpg.window(label="Entity editor", width=500, height=650):
    with dpg.group(horizontal=True):
        dpg.add_combo(["Stage 1", "Stage 2", "Stage 3", "Stage 4"])
        dpg.add_text(">")
        dpg.add_combo(["Slug", "Spider", "Ghoul"])
    dpg.add_image("entity_texture")

    with dpg.group():
        with dpg.collapsing_header(label="Attributes"):
            for attribute in dummy_attributes:
                with dpg.group(horizontal=True):
                    dpg.add_button(label=attribute)
                    dpg.add_checkbox(label="enabled")
                    dpg.add_button(label='delete')
            dpg.add_button(label='attr_pushes_player_back')
        dpg.add_button(label="Add Attribute", callback=save_callback)

    with dpg.popup(dpg.last_item(), mousebutton=dpg.mvMouseButton_Left, modal=True):
        dpg.add_button(label='attr_stage_1_collision')
        dpg.add_button(label='attr_pushes_player_back')

    with dpg.group():
        with dpg.collapsing_header(label="Components"):
            for component in dummy_components:
                with dpg.group(horizontal=True):
                    with dpg.collapsing_header(label=component):
                        for key, value in dummy_components[component].items():
                            with dpg.group(horizontal=True):
                                dpg.add_text(key)
                                dpg.add_text(value)

                    dpg.add_button(label='delete')
        dpg.add_button(label="Add Component", callback=save_callback)

    with dpg.popup(dpg.last_item(), mousebutton=dpg.mvMouseButton_Left, modal=True):
        dpg.add_button(label='emits_event_on_sight')
        dpg.add_button(label='moves')
        dpg.add_button(label='speed')
        dpg.add_button(label='velocity')

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
