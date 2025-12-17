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
        if self.frame_iteration > 100 * len(self.snake):
            reward = -10
            done = True
            return self._get_state(), reward, done, self.score
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
        head = self.head
        point_l = Point(head.x - 1, head.y)
        point_r = Point(head.x + 1, head.y)
        point_u = Point(head.x, head.y - 1)
        point_d = Point(head.x, head.y + 1)

        dir_l = self.direction == Direction.LEFT
        dir_r = self.direction == Direction.RIGHT
        dir_u = self.direction == Direction.UP
        dir_d = self.direction == Direction.DOWN

        state = [
            # danger straight
            (dir_r and self._is_collision(point_r)) or
            (dir_l and self._is_collision(point_l)) or
            (dir_u and self._is_collision(point_u)) or
            (dir_d and self._is_collision(point_d)),

            # danger right
            (dir_u and self._is_collision(point_r)) or
            (dir_d and self._is_collision(point_l)) or
            (dir_l and self._is_collision(point_u)) or
            (dir_r and self._is_collision(point_d)),

            # danger left
            (dir_d and self._is_collision(point_r)) or
            (dir_u and self._is_collision(point_l)) or
            (dir_r and self._is_collision(point_u)) or
            (dir_l and self._is_collision(point_d)),

            # move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # food location
            self.food.x < head.x,
            self.food.x > head.x,
            self.food.y < head.y,
            self.food.y > head.y
        ]

        return [int(x) for x in state]
