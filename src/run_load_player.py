import pygame
from stable_baselines3 import PPO
from game import GRID_SIZE
from game_env import MinesweeperEnv

env = MinesweeperEnv(graphics=True) # You can set graphics to False to run without visuals
env.reset()

n_steps = 39_800_000
models_dir = "../models/modelsv9/PPO"
model_path = f"{models_dir}/minesweeper_model{n_steps}"

model = PPO.load(model_path, env=env)

episodes = 1000

for ep in range(episodes):
    obs, _ = env.reset()
    done = False
    while not done:
        env.render()

        print(obs)
        action, _ = model.predict(obs)
        obs, reward, done, _, info = env.step(action)

        x, y = action % GRID_SIZE, action // GRID_SIZE

        print(f"Action: {(x, y)} reward: {reward} done: {done}")
        pygame.time.wait(1000)

env.close()