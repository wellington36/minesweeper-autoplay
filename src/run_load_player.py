import pygame
from stable_baselines3 import PPO
from game_env import MinesweeperEnv

env = MinesweeperEnv(graphics=True) # You can set graphics to False to run without visuals
env.reset()

models_dir = "../modelsv7/PPO"
model_path = f"{models_dir}/minesweeper_model2900000"

model = PPO.load(model_path, env=env)

episodes = 1000

for ep in range(episodes):
    obs, _ = env.reset()
    done = False
    while not done:
        env.render()

        action, _ = model.predict(obs)
        obs, reward, done, _, info = env.step(action)

        print(f"Action: {action} reward: {reward} done: {done}")
        pygame.time.wait(1000)

env.close()