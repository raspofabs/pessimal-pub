from pessimal.v2 import V2
from pessimal.camera import Camera2D

def test_camera_construction():
    display_size = V2(22,44)

    cam = Camera2D(display_size=display_size)
    assert cam.display_size == display_size
    assert cam.scale == 1.0
    assert cam.top_left == display_size * -0.5

    cam = Camera2D()
    assert cam.display_size != display_size
    assert cam.scale == 1.0
    assert cam.top_left != display_size * -0.5

def test_set_display():
    cam = Camera2D(display_size=V2(100,100))

    assert cam.pos_to_screen(V2(0,0)) == V2(50,50)

    cam.set_display(V2(1000,1000))

    assert cam.pos_to_screen(V2(0,0)) == V2(500,500)


def test_centre_on():
    pass

def test_conversions():
    cam = Camera2D(display_size=V2(100,100))

    pos = V2(10,10)
    screen_pos = cam.pos_to_screen(pos)
    assert screen_pos == V2(60, 60)
    assert cam.screen_to_pos(screen_pos) == pos

    size = 100
    screen_size = cam.size_to_screen(size)
    assert screen_size == 100
    assert size == cam.screen_to_size(screen_size)

    # test scaled conversions

    # should map 0-10 -> 0-100
    cam.centre_on(V2(5,5), 10)

    screen_pos = cam.pos_to_screen(pos)
    assert screen_pos == V2(100, 100)

    screen_size = cam.size_to_screen(size)
    assert screen_size == 1000

    assert cam.screen_to_pos(screen_pos) == pos
    assert size == cam.screen_to_size(screen_size)

