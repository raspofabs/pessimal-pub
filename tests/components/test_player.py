from pessimal.components import Player
from pessimal.component import Component
from pessimal.v2 import V2

from tests.fixtures import f_mock_engine
from tests.components.fixtures import f_simple_world

import pytest


@pytest.fixture
def f_player_config():
    return {
        "type": "Entity",
        "name": "MyPlayer",
        "size": 16.0,
        "start_pos": "[0.00, 0.00]",
        "components": [
            {
                "type": "Player",
                "which_player": 2,
            },
        ],
    }


def test_player(f_mock_engine, f_simple_world, f_player_config):
    player_entity = f_simple_world.add_entity(f_player_config)
    assert player_entity is not None

    oc = player_entity.get_component("Player")
    assert oc is not None

    assert oc.which_player == 2
