from fixtures import f_mock_engine

from pessimal.game import Game

import pygame


def test_game(f_mock_engine):
    game = Game(
        f_mock_engine, config={"start_world": "tests/test_data/test_world.yaml"}
    )

    game.save_config()
    game.start()
    game.stop()
    game.update(1.0)
    game.render(f_mock_engine)

    f_mock_engine.run()

    game.process_event(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_UP}))
    game.process_event(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN}))
    game.process_event(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LEFT}))
    game.process_event(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT}))

    game.update(1.0)
    game.render(f_mock_engine)

    game.process_event(pygame.event.Event(pygame.KEYUP, {"key": pygame.K_UP}))
    game.process_event(pygame.event.Event(pygame.KEYUP, {"key": pygame.K_DOWN}))
    game.process_event(pygame.event.Event(pygame.KEYUP, {"key": pygame.K_LEFT}))
    game.process_event(pygame.event.Event(pygame.KEYUP, {"key": pygame.K_RIGHT}))

    game.process_event(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_F5}))
    game.process_event(pygame.event.Event(pygame.KEYUP, {"key": pygame.K_F5}))

    game.update(1.0)
    game.render(f_mock_engine)

    game.process_event(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_EQUALS}))
    game.process_event(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_MINUS}))
    game.process_event(pygame.event.Event(pygame.QUIT, {}))

    game.update(1.0)
    game.render(f_mock_engine)

    game.process_event(pygame.event.Event(pygame.KEYUP, {"key": pygame.K_EQUALS}))
    game.process_event(pygame.event.Event(pygame.KEYUP, {"key": pygame.K_MINUS}))
    game.process_event(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE}))
    game.process_event(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_q}))

    game.update(1.0)
    game.render(f_mock_engine)
