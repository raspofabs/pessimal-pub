from pessimal.components import Orbiter
from pessimal.component import Component
from pessimal.v2 import V2

from tests.fixtures import f_mock_engine
from tests.components.fixtures import f_simple_world

import pytest


@pytest.fixture
def f_orbiter_config():
    return {
        "type": "Entity",
        "name": "MyOrbiter",
        "size": 16.0,
        "start_pos": "[0.00, 0.00]",
        "components": [
            {
                "type": "Orbiter",
                "speed": 40,
                "centre": "[0.00, 0.00]",
                "radius": 32,
            },
        ],
    }


def test_orbiter(f_mock_engine, f_simple_world, f_orbiter_config):
    orbiter_entity = f_simple_world.add_entity(f_orbiter_config)
    assert orbiter_entity is not None

    oc = orbiter_entity.get_component("Orbiter")
    assert oc is not None


def test_orbiter_update(f_mock_engine, f_orbiter_config, f_simple_world):
    f_simple_world.add_entity(f_orbiter_config)

    # intial step to move to start position
    f_simple_world.update(0.1)

    # subsequent step
    f_simple_world.update(0.1)
