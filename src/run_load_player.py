import pygame
from stable_baselines3 import PPO
from game_env import MinesweeperEnv

env = MinesweeperEnv(graphics=True) # You can set graphics to False to run without visuals
env.reset(seed=42)

models_dir = "../modelsv2/PPO"
model_path = f"{models_dir}/minesweeper_model490000.zip"

model = PPO.load(model_path, env=env)

episodes = 10

for ep in range(episodes):
    obs, _ = env.reset(seed=42)
    done = False
    while not done:
        env.render()
        action, _ = model.predict(obs)
        obs, reward, done, _, info = env.step(action)
        pygame.time.wait(10)

env.close()