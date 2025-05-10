from linflex import clamp, sign, lerp, move_toward


def test_clamp():
    assert clamp(7, 5, 10) == 7
    assert clamp(7, 2, 5) == 5
    assert clamp(7, 4, 6) == 6
    assert clamp(7, 9, 10) == 9
    # NOTE: This one should *also* give a lint error if `float` and `int` are mixed
    assert isinstance(clamp(7, 9.0, 10), float)


def test_sign():
    assert sign(0) == 0
    assert sign(-1) == -1
    assert sign(1) == 1
    assert sign(5) == 1
    assert sign(-5) == -1
    assert sign(3.5) == 1
    assert sign(-3.5) == -1


def test_lerp():
    assert lerp(0, 10, 0.50) == 5
    assert lerp(0, -10, 0.50) == -5
    assert lerp(0, 1, 0.50) == 0.5
    assert lerp(-10, -20, 0.50) == -15
    assert lerp(20, -20, 0.50) == 0


def test_move_toward():
    assert move_toward(0, 10, 1) == 1
    assert move_toward(0, 10, 10) == 10
    assert move_toward(0, 10, 15) == 10
    assert move_toward(10, 0, 1) == 9
    assert move_toward(10, 0, 10) == 0
    assert move_toward(10, 0, 15) == 0
    assert move_toward(5, 5, 1) == 5
    assert move_toward(5.0, 10.0, 2.5) == 7.5
    assert move_toward(10.0, 5.0, 2.5) == 7.5
