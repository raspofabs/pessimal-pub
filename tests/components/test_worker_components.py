from pessimal.components import Worker
from pessimal.component import Component
from pessimal.v2 import V2

from tests.fixtures import f_mock_engine
from tests.components.fixtures import f_simple_world
from tests.components.test_world_resource import f_world_resource_config

import copy
import pytest


@pytest.fixture
def f_workcenter_config():
    return {
        "type": "Entity",
        "name": "BytesRUs",
        "size": 16.0,
        "start_pos": "[16.00, 0.00]",
        "components": [
            {
                "type": "Building",
                "name": "Office",
                "depth": 1,
                "storeys": 1,
                "width": 2,
                "door_x_pos": 1,
            },
            {
                "type": "WorkCentre",
                "job": "Coder",
                "inventory_limit": 3,
                "inputs": [
                    "client request",
                ],
                "products": [
                    "software",
                ],
            },
        ],
    }


@pytest.fixture
def f_worker_config():
    return {
        "type": "Entity",
        "name": "Bill",
        "size": 16.0,
        "start_pos": "[0.00, 16.00]",
        "components": [
            {
                "type": "Character",
                "variant": "keyboard",
                "speed": 40,
            },
            {
                "type": "Worker",
                "job": "Coder",
                "workcentre": "BytesRUs",
            },
        ],
    }


@pytest.fixture
def f_world_setup(
    f_mock_engine,
    f_simple_world,
    f_world_resource_config,
    f_workcenter_config,
    f_worker_config,
):
    worker_entity = f_simple_world.add_entity(f_worker_config)
    assert worker_entity is not None

    workcentre_entity = f_simple_world.add_entity(f_workcenter_config)
    assert workcentre_entity is not None

    world_resource_entity = f_simple_world.add_entity(f_world_resource_config)
    assert world_resource_entity is not None

    return f_simple_world


def test_worker(f_mock_engine, f_world_setup):
    world = f_world_setup
    worker_entity = world.find_entity_by_name("Bill")
    assert worker_entity is not None
    workcentre_entity = world.find_entity_by_name("BytesRUs")
    assert workcentre_entity is not None
    world_resource_entity = world.find_entity_by_name("Client")
    assert world_resource_entity is not None

    wc = worker_entity.get_component("Worker")
    assert wc is not None

    wcc = workcentre_entity.get_component("WorkCentre")
    assert wcc is not None

    wrc = world_resource_entity.get_component("WorldResource")
    assert wrc is not None

    assert "WorkerState" in str(wc)

    worker_workcentre = wc.get_workcentre_entity()
    assert worker_workcentre is not None

    assert wcc == wc.get_workcentre()
    assert "Coder" in str(wcc)
    assert "software" in str(wcc)
    assert "client request" in str(wcc)

    # test worker progress

    assert "RESTING" in str(wc)
    assert worker_entity.pos == V2(0, 16)
    world.update(1.0)

    # commute to work
    assert "COMMUTING" in str(wc)
    assert worker_entity.pos == V2(0, 16)
    world.update(0.0)
    world.update(1.0)
    assert worker_entity.pos == V2(32, 0)

    # THINK
    assert "THINKING" in str(wc)
    world.update(2.0)

    # FETCHING_MATERIALS
    assert "FETCHING_MATERIALS" in str(wc)

    for _ in range(100):
        world.update(0.5)
        f_mock_engine.toggle_culling()
        world.render(f_mock_engine)


def test_no_resources(f_mock_engine, f_world_setup):
    world = f_world_setup
    worker_entity = world.find_entity_by_name("Bill")
    assert worker_entity is not None
    workcentre_entity = world.find_entity_by_name("BytesRUs")
    assert workcentre_entity is not None

    wc = worker_entity.get_component("Worker")
    assert wc is not None

    # test worker progress without resource

    assert "RESTING" in str(wc)
    assert worker_entity.pos == V2(0, 16)
    world.update(1.0)

    # commute to work
    assert "COMMUTING" in str(wc)
    assert worker_entity.pos == V2(0, 16)
    world.update(0.0)
    world.update(1.0)
    assert worker_entity.pos == V2(32, 0)

    # THINK
    assert "THINKING" in str(wc)
    world.update(1.0)

    # can't fetch materials
    assert "FETCHING_MATERIALS" not in str(wc)


def test_reward_effort_without_correct_state(f_mock_engine, f_world_setup):
    world = f_world_setup
    worker_entity = world.find_entity_by_name("Bill")

    wc = worker_entity.get_component("Worker")
    wcc = wc.get_workcentre()

    wc_before = copy.deepcopy(wc)
    wcc_before = copy.deepcopy(wcc)

    assert wc.carrying == wc_before.carrying
    assert wcc.inventory == wcc_before.inventory
    assert wcc.stock == wcc_before.stock
    wc.reward_effort()
    assert wc.carrying == wc_before.carrying
    assert wcc.inventory == wcc_before.inventory
    assert wcc.stock == wcc_before.stock


def test_having_a_think_with_next_state(f_mock_engine, f_world_setup):
    world = f_world_setup
    worker_entity = world.find_entity_by_name("Bill")

    wc = worker_entity.get_component("Worker")
    wc.have_a_think(10.0)


def test_output_is_full(f_mock_engine, f_world_setup):
    world = f_world_setup
    worker_entity = world.find_entity_by_name("Bill")
    assert worker_entity is not None
    workcentre_entity = world.find_entity_by_name("BytesRUs")
    assert workcentre_entity is not None
    world_resource_entity = world.find_entity_by_name("Client")
    assert world_resource_entity is not None

    wc = worker_entity.get_component("Worker")
    assert wc is not None

    wcc = workcentre_entity.get_component("WorkCentre")
    assert wcc is not None
    wcc.inventory_limit = 1

    # test worker progress

    assert "RESTING" in str(wc)
    assert worker_entity.pos == V2(0, 16)
    world.update(1.0)

    # commute to work
    assert "COMMUTING" in str(wc)
    assert worker_entity.pos == V2(0, 16)
    world.update(0.0)
    world.update(1.0)
    assert worker_entity.pos == V2(32, 0)

    # THINK
    assert "THINKING" in str(wc)
    world.update(2.0)

    # FETCHING_MATERIALS
    assert "FETCHING_MATERIALS" in str(wc)
    world.update(1.0)
    world.update(1.0)
    world.update(1.0)
    assert "COMMUTING" in str(wc)
    world.update(1.0)
    world.update(1.0)
    world.update(1.0)
    assert "THINKING" in str(wc)
    world.update(1.0)
    assert "WORKING" in str(wc)
    world.update(1.0)
    world.update(1.0)
    assert "FETCHING_MATERIALS" in str(wc)
    world.update(1.0)
    world.update(1.0)
    world.update(1.0)
    assert "COMMUTING" in str(wc)
    world.update(1.0)
    world.update(1.0)
    world.update(1.0)
    assert "THINKING" in str(wc)
    world.update(1.0)
    assert "WORKING" in str(wc)
    world.update(1.0)

    # stuck while inventory_limit is reached
    for _ in range(100):
        assert "THINKING" in str(wc)
        world.update(0.5)
        f_mock_engine.toggle_culling()
        world.render(f_mock_engine)


def test_task_pop_in_regular_update(f_mock_engine, f_world_setup):
    world = f_world_setup
    worker_entity = world.find_entity_by_name("Bill")

    wc = worker_entity.get_component("Worker")
    wc.task_queue.append(Worker.gather)
    world.update(0.5)


# TODO: add recipes
def test_recipes():
    pass


# TODO: add delivering
def test_delivering():
    pass
