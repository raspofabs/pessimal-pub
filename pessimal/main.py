# pragma: exclude file
# main requires full running window and OpenGL

from pessimal.game import Game
from pessimal.editor import Editor
from pessimal.engine import Engine


def run():
    engine = Engine()
    game = Game(engine)
    editor = Editor(engine, game)

    last_error = None
    while engine.running:
        try:
            engine.tick()
            last_error = None
        except NameError as e:
            if str(e) != str(last_error):
                print(f"New root error: {e}")
            last_error = e
            raise e

    engine.shutdown()


if __name__ == '__main__':
    run()
