from typing import List
import dearpygui.dearpygui as dpg
import tomlkit
import os

# TODO - move to config somewhere
unit_stage_dir = '/home/joe/code/mr-figs/src/units'

def delete_attribute(sender, app_data):
    attribute = sender.split(':')[1]
    dpg.delete_item('row:' + attribute)

def get_entities_for_stage(stage: str, unit_type: str) -> List[str]:
    print(unit_stage_dir, stage, unit_type)
    print([unit for unit in os.listdir(unit_stage_dir + '/' + stage + '/' + unit_type)])
    return [unit for unit in os.listdir(unit_stage_dir + '/' + stage + '/' + unit_type)]

def change_current_stage(sender, app_data):
    unit_type = dpg.get_value('type_selection')
    entities = get_entities_for_stage(app_data, unit_type)
    dpg.configure_item("entity_selection", default_value=entities[0])
    dpg.configure_item("entity_selection", items=entities)

def change_current_type(sender, app_data):
    unit_type = dpg.get_value('type_selection')
    stage = dpg.get_value('stage_selection')
    entities = get_entities_for_stage(stage, unit_type)
    dpg.configure_item("entity_selection", default_value=entities[0])
    dpg.configure_item("entity_selection", items=entities)

def get_current_entity_data(sender, app_data) -> str:
    selected_stage = dpg.get_value('stage_selection')
    selected_type = dpg.get_value('type_selection')
    selected_entity = dpg.get_value('entity_selection')
    return tomlkit.loads(open(unit_stage_dir + '/' + selected_stage + '/' + selected_type + '/' + selected_entity).read())

stages = [stage for stage in os.listdir(unit_stage_dir)]
stages.sort()

current_stage = stages[0]

unit_types = [types for types in os.listdir(unit_stage_dir + '/' + current_stage)]
unit_types.sort()

current_type = unit_types[0]

entities = get_entities_for_stage(current_stage, current_type)

entity = tomlkit.loads(open(unit_stage_dir + '/' + current_stage + '/' + current_type + '/' + entities[0]).read())

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

attributes = tomlkit.loads(open('test-attributes.toml').read())
components = tomlkit.loads(open('test-components.toml').read())

width, height, channels, data = dpg.load_image('slug.png')

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
    with dpg.group(horizontal=True, width=155):
        dpg.add_combo(
            stages,
            callback=change_current_stage,
            tag="stage_selection",
            default_value=current_stage
        )
        dpg.add_combo(
            unit_types,
            callback=change_current_type,
            tag="type_selection",
            default_value=current_type
        )
        dpg.add_combo(
            entities,
            callback=get_current_entity_data,
            tag="entity_selection", 
            default_value=entities[0]
        )
    dpg.add_image("entity_texture")

    # Attribute listing
    with dpg.group():
        with dpg.collapsing_header(label="Attributes"):
            with dpg.table(resizable=True, row_background=True,policy=dpg.mvTable_SizingStretchProp,
                   borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True):

                dpg.add_table_column(label="Name")
                dpg.add_table_column(label="Enabled?")
                dpg.add_table_column(label="Delete?")

                for key, value in entity['attributes'].items(): 
                    with dpg.table_row(tag="row:" + key):
                        with dpg.table_cell():
                            dpg.add_text(key, tag="button:" + key)
                        with dpg.table_cell():
                            checkbox_label = "enabled" if bool(value) else "disabled"
                            dpg.add_checkbox(label=checkbox_label, tag="checkbox:" + key, default_value=bool(value))
                        with dpg.table_cell():
                            dpg.add_button(label='delete', callback=delete_attribute, tag="delete:" + key)
                            dpg.bind_item_theme(dpg.last_item(), warning_theme)
            dpg.add_button(label="Add Attribute")
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
            for component in entity['component']:
                with dpg.group(horizontal=True):
                    with dpg.collapsing_header(label=component, indent=12):
                        for key, value in entity['component'][component].items(): #components[component].items():
                            with dpg.group(horizontal=True):
                                dpg.add_text(key + ':')
                                if components[component][key] == 'int':
                                    dpg.add_input_int(default_value=value)
                                elif components[component][key] == 'string':
                                    dpg.add_input_text(default_value=value)
                                elif type(components[component][key]) == tomlkit.items.Array:
                                    dpg.add_combo(components[component][key])
                                else:
                                    dpg.add_text(value)

                        dpg.add_button(label='delete')
                        dpg.bind_item_theme(dpg.last_item(), warning_theme)
        dpg.add_button(label="Add Component")
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
