import dearpygui.dearpygui as dpg
import tomlkit

def save_callback():
    print("Save Clicked")

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()


attributes = tomlkit.loads(open('test-attributes.toml').read())
components = tomlkit.loads(open('test-components.toml').read())


width, height, channels, data = dpg.load_image("slug.png")

with dpg.theme() as warning_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (175, 0, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (225, 0, 0), category=dpg.mvThemeCat_Core)

with dpg.theme() as action_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 125, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 175, 0), category=dpg.mvThemeCat_Core)


with dpg.texture_registry():
    dpg.add_static_texture(width=width, height=height, default_value=data, tag="entity_texture")

with dpg.window(label="Entity editor", width=500, height=650):
    with dpg.group(horizontal=True):
        dpg.add_combo(["Stage 1", "Stage 2", "Stage 3", "Stage 4"])
        dpg.add_text(">")
        dpg.add_combo(["Slug", "Spider", "Ghoul"])
    dpg.add_image("entity_texture")

    # Attribute listing
    with dpg.group():
        with dpg.collapsing_header(label="Attributes"):
            for attribute in attributes:
                with dpg.group(horizontal=True, indent=12):
                    dpg.add_button(label=attribute)
                    dpg.add_checkbox(label="enabled")
                    dpg.add_button(label='delete')
        dpg.add_button(label="Add Attribute", callback=save_callback)
        dpg.bind_item_theme(dpg.last_item(), action_theme)

    # Attribute popup
    with dpg.popup(dpg.last_item(), mousebutton=dpg.mvMouseButton_Left):
        for attribute in attributes:
            dpg.add_button(label=attribute, tag=attribute)

            with dpg.tooltip(attribute):
                dpg.add_text(attributes[attribute]['description'])

    # Component listing
    with dpg.group():
        with dpg.collapsing_header(label="Components"):
            for component in components:
                with dpg.group(horizontal=True):
                    with dpg.collapsing_header(label=component, indent=12):
                        for key, value in components[component].items():
                            with dpg.group(horizontal=True):
                                dpg.add_text(key + ':')
                                if value == 'int':
                                    dpg.add_input_int()
                                elif value == 'string':
                                    dpg.add_input_text()
                                elif type(value) == tomlkit.items.Array:
                                    dpg.add_combo(value)
                                else:
                                    dpg.add_text(value)

                        dpg.add_button(label='delete')
                        dpg.bind_item_theme(dpg.last_item(), warning_theme)
        dpg.add_button(label="Add Component", callback=save_callback)
        dpg.bind_item_theme(dpg.last_item(), action_theme)

    # Component popup
    with dpg.popup(dpg.last_item(), mousebutton=dpg.mvMouseButton_Left):
        for component in components:
            dpg.add_button(label=component, tag=component)

            with dpg.tooltip(component):
                dpg.add_text(components[component]['description'])

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
