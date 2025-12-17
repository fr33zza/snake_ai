import random
from collections import deque
from game.constants import Direction, Point


class SnakeGame:
    def __init__(self, w=20, h=20):
        self.w = w
        self.h = h
        # inicjalizacja atrybutów (dla lintera i czytelności)
        self.direction = None
        self.head = None
        self.snake = None
        self.food = None
        self.score = 0
        self.frame_iteration = 0
        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(self.w // 2, self.h // 2)
        self.snake = deque([
            self.head,
            Point(self.head.x - 1, self.head.y),
            Point(self.head.x - 2, self.head.y)
        ])

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

        return self._get_state()

    def _place_food(self):
        while True:
            x = random.randint(0, self.w - 1)
            y = random.randint(0, self.h - 1)
            self.food = Point(x, y)
            if self.food not in self.snake:
                break

    def step(self, action):
        """
        action:
        0 = skręt w lewo
        1 = prosto
        2 = skręt w prawo
        """
        self.frame_iteration += 1
        self._move(action)
        self.snake.appendleft(self.head)

        reward = 0
        done = False

        if self._is_collision():
            reward = -10
            done = True
            return self._get_state(), reward, done, self.score

        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        return self._get_state(), reward, done, self.score

    def _is_collision(self, point=None):
        if point is None:
            point = self.head

        # ściana
        if point.x < 0 or point.x >= self.w or point.y < 0 or point.y >= self.h:
            return True

        # ciało
        if point in list(self.snake)[1:]:
            return True

        return False

    def _move(self, action):
        clockwise = [
            Direction.RIGHT,
            Direction.DOWN,
            Direction.LEFT,
            Direction.UP
        ]

        idx = clockwise.index(self.direction)

        if action == 0:  # lewo
            new_dir = clockwise[(idx - 1) % 4]
        elif action == 1:  # prosto
            new_dir = clockwise[idx]
        else:  # prawo
            new_dir = clockwise[(idx + 1) % 4]

        self.direction = new_dir

        x, y = self.head
        if self.direction == Direction.RIGHT:
            x += 1
        elif self.direction == Direction.LEFT:
            x -= 1
        elif self.direction == Direction.UP:
            y -= 1
        elif self.direction == Direction.DOWN:
            y += 1

        self.head = Point(x, y)

    def _get_state(self):
        """
        Na razie zwracamy minimalny placeholder.
        Docelowo tu będzie stan pod AI.
        """
        return {
            "head": self.head,
            "food": self.food,
            "direction": self.direction,
            "snake": list(self.snake)
        }
