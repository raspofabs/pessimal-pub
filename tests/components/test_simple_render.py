from pessimal.components import SimpleRender
from pessimal.component import Component
from pessimal.v2 import V2

from tests.fixtures import f_mock_engine
from tests.components.fixtures import f_simple_world

import pytest


@pytest.fixture
def f_simple_render_config():
    return {
        "type": "Entity",
        "name": "Blue",
        "size": 16.0,
        "start_pos": '[0.00, 0.00]',
        "components":[
            {
                "type": "SimpleRender",
                "colour": "(30, 90, 200)",
                }
            ],
        }

def test_simple_render(f_mock_engine, f_simple_world, f_simple_render_config):
    simple_render_entity = f_simple_world.add_entity(f_simple_render_config)
    assert simple_render_entity is not None

    cc = simple_render_entity.get_component("SimpleRender")
    assert cc is not None


def test_simple_render_render(f_mock_engine, f_simple_render_config, f_simple_world):
    f_simple_world.add_entity(f_simple_render_config)

    # default render
    f_simple_world.render(f_mock_engine)

    # not rendering
    f_mock_engine.toggle_culling()
    f_simple_world.render(f_mock_engine)

