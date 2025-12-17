import random
from game.snake_game import SnakeGame

if __name__ == "__main__":
    game = SnakeGame()

    state = game.reset()
    print(state)  # powinno wypisać 11 liczb (0/1)

    for _ in range(10):
        s, r, d, score = game.step(random.randint(0, 2))
        print(s, r)
        if d:
            print("GAME OVER")
            break