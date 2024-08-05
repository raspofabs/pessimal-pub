from pessimal.components import Character
from pessimal.component import Component
from pessimal.v2 import V2

from tests.fixtures import f_mock_engine
from tests.components.fixtures import f_simple_world

import pytest


@pytest.fixture
def f_character_config():
    return {
        "type": "Entity",
        "name": "Brad",
        "size": 16.0,
        "start_pos": '[0.00, 0.00]',
        "components":[
            {
                "type": "Character",
                "speed": 40,
                "variant": "pick",
                "rseed": 1,
                }
            ],
        }

def test_character_variants():
    assert Character.get_tool_sprite_id("pick") is not None
    assert Character.get_tool_sprite_id("axe") is not None
    assert Character.get_tool_sprite_id("unknown") is None


def test_character(f_mock_engine, f_simple_world, f_character_config):
    character_entity = f_simple_world.add_entity(f_character_config)
    assert character_entity is not None

    cc = character_entity.get_component("Character")
    assert cc is not None

    assert cc.body_variant == 0
    assert cc.shoes_variant == 1
    assert cc.trousers_variant == 5
    assert cc.torso_variant == (7, 7)
    assert cc.hair_colour == (4, 4)
    assert cc.hair_variant1 == (26, 5)
    assert cc.hair_variant2 == (23, 7)


@pytest.mark.parametrize("seed", [1,2,3,4, 10, 20, 80, 100])
def test_character_seeds(f_mock_engine, f_simple_world, f_character_config, seed):
    f_character_config["components"][0]["rseed"] = seed
    character_entity = f_simple_world.add_entity(f_character_config)
    assert character_entity is not None
    cc = character_entity.get_component("Character")


def test_character_control(f_mock_engine, f_simple_world, f_character_config):
    character_entity = f_simple_world.add_entity(f_character_config)
    assert character_entity is not None

    cc = character_entity.get_component("Character")
    assert cc is not None

    cc.go_to(V2(10,10))
    assert cc.destination is not None
    # move a little
    f_simple_world.update(0.1)
    assert cc.destination is not None
    # move a lot
    f_simple_world.update(1.0)
    assert cc.destination is None
    # stand still
    f_simple_world.update(0.1)
    assert cc.destination is None



def test_character_render(f_mock_engine, f_character_config, f_simple_world):
    f_simple_world.add_entity(f_character_config)

    # default render
    f_simple_world.render(f_mock_engine)

    # not rendering
    f_mock_engine.toggle_culling()
    f_simple_world.render(f_mock_engine)


from tests.components.test_road_network import f_road_config
def test_character_on_road(f_mock_engine, f_character_config, f_simple_world, f_road_config):

    character_entity = f_simple_world.add_entity(f_character_config)
    assert character_entity is not None

    cc = character_entity.get_component("Character")
    assert cc is not None

    cc.go_to(V2(40,40))

    # add a toolless character
    f_character_config["name"] = "NoneKin"
    f_character_config["components"][0]["variant"] = "unknown"
    character_entity = f_simple_world.add_entity(f_character_config)
    assert character_entity is not None

    # add the roads
    f_simple_world.add_entity(f_road_config)

    # update to generate debug arrows
    f_simple_world.update(0.1)

    # render everything
    f_simple_world.render(f_mock_engine)


