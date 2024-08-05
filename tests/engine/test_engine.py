from pessimal.engine import EngineDependent, Engine, SystemStatus

from tests.fixtures import f_mock_engine
import pytest


def test_dependent(f_mock_engine):
    simple_dependent = EngineDependent(f_mock_engine)

    simple_dependent.process_event(None)
    simple_dependent.start()
    simple_dependent.stop()
    simple_dependent.update(0.1)
    simple_dependent.render(f_mock_engine)


@pytest.mark.gui
def test_engine():
    engine = Engine()
    simple_dependent = EngineDependent(engine)

    engine.switch_status(SystemStatus.EDITING)
    engine.switch_status(SystemStatus.RUNNING)
    engine.switch_status(SystemStatus.PAUSED)
    engine.switch_status(SystemStatus.RUNNING)
    for _ in range(5):
        engine.clear_screen((20,20,20))
        engine.tick()
        engine.end_frame()
    engine.should_show_demo = True
    for _ in range(5):
        engine.clear_screen((20,20,20))
        engine.tick()
        engine.end_frame()

@pytest.mark.gui
def test_simple_game_setup():
    # setup simple world
    # open editor
    # change modes
    pass
