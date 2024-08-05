from pessimal.components import WorldResource
from pessimal.component import Component
from pessimal.v2 import V2

from tests.fixtures import f_mock_engine
from tests.components.fixtures import f_simple_world

import pytest


@pytest.fixture
def f_world_resource_config():
    return {
        "type": "Entity",
        "name": "Client",
        "size": 16.0,
        "start_pos": '[0.00, 0.00]',
        "components":[
            {
                "type": "WorldResource",
                "kind": "client request",
                "quantity": 2,
                },
            ],
        }


def test_world_resource(f_mock_engine, f_simple_world, f_world_resource_config):
    world_resource_entity = f_simple_world.add_entity(f_world_resource_config)
    assert world_resource_entity is not None

    oc = world_resource_entity.get_component("WorldResource")
    assert oc is not None

    assert oc.kind == "client request"
    assert oc.quantity == 2

    oc.current_quantity = 1

    assert "client request - 1/2" in str(oc)
    oc.start()
    assert "client request - 2/2" in repr(oc)
