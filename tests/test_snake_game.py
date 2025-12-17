import pytest
from game.snake_game import SnakeGame
from game.constants import Direction, Point


def test_reset():
    game = SnakeGame(10, 10)
    state = game.reset()

    assert game.score == 0
    assert len(game.snake) == 3
    assert len(state) == 11


def test_move_forward():
    game = SnakeGame(10, 10)
    game.reset()
    head_before = game.head

    state, reward, done, score = game.step(1)  # prosto

    assert game.head != head_before
    assert done is False


def test_eat_food():
    game = SnakeGame(10, 10)
    game.reset()

    # ustaw jedzenie tuż przed głową
    head = game.head
    game.food = Point(head.x + 1, head.y)

    state, reward, done, score = game.step(1)

    assert reward == 10
    assert score == 1
    assert len(game.snake) == 4


def test_wall_collision():
    game = SnakeGame(5, 5)
    game.reset()

    game.head = Point(4, 2)
    game.direction = Direction.RIGHT

    state, reward, done, score = game.step(1)

    assert done is True
    assert reward == -10


def test_state_length():
    game = SnakeGame()
    state = game.reset()
    assert len(state) == 11


def test_timeout():
    game = SnakeGame(10, 10)
    game.reset()

    game.frame_iteration = 100 * len(game.snake) + 1
    state, reward, done, score = game.step(1)

    assert done is True
    assert reward == -10
