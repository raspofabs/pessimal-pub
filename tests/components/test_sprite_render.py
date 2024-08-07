from pessimal.components import SpriteRender
from pessimal.component import Component
from pessimal.v2 import V2

from tests.fixtures import f_mock_engine
from tests.components.fixtures import f_simple_world

import pytest


@pytest.fixture
def f_sprite_config():
    return {
        "type": "Entity",
        "name": "PathTee",
        "size": 16.0,
        "start_pos": "[0.00, 0.00]",
        "components": [
            {
                "type": "SpriteRender",
                "sprite_id": "1bit:path_tee",
            }
        ],
    }


def test_sprite(f_mock_engine, f_simple_world, f_sprite_config):
    sprite_entity = f_simple_world.add_entity(f_sprite_config)
    assert sprite_entity is not None

    cc = sprite_entity.get_component("SpriteRender")
    assert cc is not None


def test_sprite_render(f_mock_engine, f_sprite_config, f_simple_world):
    f_simple_world.add_entity(f_sprite_config)

    # add a SpriteRender without a valid sprite
    f_sprite_config["components"][0]["sprite_id"] = "unknown"
    f_simple_world.add_entity(f_sprite_config)

    # default render
    f_simple_world.render(f_mock_engine)

    # now without lazy asset loading
    f_simple_world.render(f_mock_engine)

    # not rendering
    f_mock_engine.toggle_culling()
    f_simple_world.render(f_mock_engine)
