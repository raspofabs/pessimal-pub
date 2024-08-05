# pragma: exclude file
# As I'm not sure how to test imgui, I will ignore this file for now.

import pygame
import yaml
import i18n

import imgui
from imgui.core import ImGuiError

from pessimal.engine import EngineDependent, SystemStatus
from pessimal.v2 import V2
from pessimal.component import Component
from pessimal.field import Field, FloatField, IntField, V2Field
from pessimal.entity import Entity

class Editor(EngineDependent):
    def __init__(self, engine, game):
        super().__init__(engine)
        self.game = game

        # do we really need this here as well?
        with open("data/setup.yaml") as yaml_fh:
            setup_data = yaml.safe_load(yaml_fh)

        self.show_editor = False
        self.selected_entity_or_component = None
        self.entity_filter = ""
        self.new_entity_name = "unnamed"
        self.last_error = None

    def update(self, dt):
        try:
            if self.show_editor:
                imgui.begin("Editor", flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE)
                self.editor_view()
                imgui.end()
            self.last_error = None
        except ImGuiError as e:
            if str(e) != str(self.last_error):
                print(f"New Error: {e}")
            self.last_error = e

    def handle_field(self, component, field):
        current_value = field.get_value(component)
        changed, new_value = False, None

        if hasattr(field, "edit"):
            field.edit(component)
        else:
            if current_value is None:
                current_value = "None"
            changed, new_value = imgui.input_text(field.name, current_value)
            if changed:
                print(f"NEW: {new_value}")
                field.set_value(component, new_value)

    def handle_component(self, component):
        for field in component.fields:
            self.handle_field(component, field)

    def editor_view(self): 
        component_types = Component.get_all_component_types()

        if imgui.button(i18n.t("ui.hello_button")):
            print('Hello editor!')
        with imgui.begin_group():
            if imgui.button(i18n.t("ui.play")):
                self.engine.switch_status(SystemStatus.RUNNING)
            imgui.same_line()
            if imgui.button(i18n.t("ui.pause")):
                self.engine.switch_status(SystemStatus.PAUSED)
            imgui.same_line()
            if imgui.button(i18n.t("ui.edit")):
                self.engine.switch_status(SystemStatus.EDITING)
            imgui.same_line()
            if imgui.button(i18n.t("ui.save")):
                self.game.save_config()
        with imgui.begin_group():
            imgui.text("World")
            imgui.same_line()
            _, self.entity_filter = imgui.input_text("filter entities", self.entity_filter)
            _, self.new_entity_name = imgui.input_text("Name", self.new_entity_name)
            imgui.same_line()
            if imgui.button("Create Entity"):
                self.game.world.add_entity({"name": self.new_entity_name})
            for entity in self.game.world.entities:
                selected = entity == self.selected_entity_or_component
                selected_flag = imgui.TREE_NODE_SELECTED if selected else 0
                if self.entity_filter and self.entity_filter.lower() not in entity.name.lower():
                    continue
                entity_open = imgui.tree_node(f"{entity.name}", selected_flag|imgui.TREE_NODE_OPEN_ON_ARROW|imgui.TREE_NODE_OPEN_ON_DOUBLE_CLICK)
                with imgui.begin_popup_context_item(str(id(entity)), mouse_button=2) as popup:
                    if popup.opened:
                        clicked, state = imgui.menu_item("Delete entity")
                        if clicked:
                            print(f"delete entity : {entity.name}")
                            self.game.world.delete_entity(entity)
                        self.engine.push_font_bold()
                        imgui.text("Add component:")
                        imgui.pop_font()
                        imgui.indent()
                        for component_type in component_types:
                            clicked, state = imgui.menu_item(f"{component_type.__name__}")
                            if clicked:
                                print(f"new component : {component_type.__name__}")
                                new_component = component_type(entity, {})
                                entity.components.append(new_component)
                if imgui.is_item_clicked():
                    self.selected_entity_or_component = entity
                if entity_open:
                    self.handle_component(entity)
                    for component in entity.components:
                        selected = component == self.selected_entity_or_component
                        selected_flag = imgui.TREE_NODE_SELECTED if selected else 0
                        component_open = imgui.tree_node(f"{component.__class__.__name__}", selected_flag|imgui.TREE_NODE_OPEN_ON_ARROW|imgui.TREE_NODE_OPEN_ON_DOUBLE_CLICK)
                        if imgui.is_item_clicked():
                            self.selected_entity_or_component = component
                        if component_open:
                            self.handle_component(component)
                            imgui.tree_pop()
                    imgui.tree_pop()

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.show_editor = not self.show_editor
