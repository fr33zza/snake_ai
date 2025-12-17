from game.snake_game import SnakeGame
import random

game = SnakeGame()

state = game.reset()
done = False

while not done:
    action = random.randint(0, 2)
    state, reward, done, score = game.step(action)
    print(f"Head: {state['head']} | Food: {state['food']} | Score: {score}")

print("Game over")