import gym
import pygame
import numpy as np
from gym import spaces
from copy import deepcopy
from game import Game as Minesweeper

MINES = 80
GRID_SIZE = 20

class MinesweeperEnv(gym.Env):
    def __init__(self, graphics=True):
        super(MinesweeperEnv, self).__init__()
        self.graphics = graphics
        self.minesweeper = Minesweeper(graphics=graphics)

        self.action_space = spaces.Discrete(GRID_SIZE**2)
        self.observation_space = spaces.Box(low=0, high=8, shape=(GRID_SIZE, GRID_SIZE), dtype=np.uint8)

    def reset(self):
        self.minesweeper = Minesweeper(graphics=self.graphics)
        return self.get_state()

    def step(self, action):
        x, y = action % GRID_SIZE, action // GRID_SIZE
        self.minesweeper.on_click((x, y))
        state = self.get_state()
        done = self.minesweeper.explosion or len(self.minesweeper.checked) == GRID_SIZE ** 2 - MINES
        reward = 0  # Initialize the reward to zero

        if done:
            if self.minesweeper.explosion:
                reward -= 1  # Lose
            else:
                reward += 1  # Win
        else:
            # You win +0.1 for each non-mine tile clicked
            if self.minesweeper.mines[x,y] == 0:
                reward += 0.1

        return state, reward, done, {}

    def render(self):
        if self.graphics:
            self.minesweeper.draw()

    def get_state(self):
        state = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8)
        for pos in self.minesweeper.checked:
            state[pos] = self.minesweeper.check_mines(pos)
        return state

env = MinesweeperEnv(graphics=True)  # You can set graphics to False to run without visuals

obs = env.reset()
done = False
for i in range(100):
    while not done:
        action = env.action_space.sample()  # Replace with your own action selection logic
        obs, reward, done, _ = env.step(action)
        env.render()
        pygame.time.wait(100)
    obs = env.reset()
    done = False