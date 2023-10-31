import pygame
import gymnasium as gym
import numpy as np
from gymnasium import spaces
from gymnasium.envs.registration import register
from game import Game as Minesweeper, GRID_SIZE, MINES

class MinesweeperEnv(gym.Env):
    def __init__(self, graphics=True):
        super(MinesweeperEnv, self).__init__()
        self.graphics = graphics
        self.minesweeper = Minesweeper(graphics=graphics)

        self.action_space = spaces.Discrete(GRID_SIZE**2)
        self.observation_space = spaces.Box(low=0, high=8, shape=(GRID_SIZE * GRID_SIZE,), dtype=np.uint8)  # Flatten the observation space

    def reset(self, seed=None, options=None):
        self.minesweeper = Minesweeper(graphics=self.graphics)
        self.reward = 0  # Initialize the reward to zero
        return self.get_state(), {}

    def step(self, action):
     self.render()
     x, y = action % GRID_SIZE, action // GRID_SIZE
     self.minesweeper.on_click((x, y))
     state = self.get_state()
     done = self.minesweeper.explosion or len(self.minesweeper.checked) == GRID_SIZE ** 2 - MINES

     if done:
         if self.minesweeper.explosion:
             self.reward -= 1  # Lose
         else:
             self.reward += 1  # Win
     else:
         # You win +0.1 for each non-mine tile clicked
         if self.minesweeper.mines[x, y] == 0:
             self.reward += 0.1

     return state, self.reward, done, done, {}  # Return a tuple of (observation, reward, done, info)

    def render(self):
        if self.graphics:
            self.minesweeper.draw()

    def get_state(self):
        state = np.zeros(GRID_SIZE * GRID_SIZE, dtype=np.uint8)
        for pos in self.minesweeper.checked:
            state[pos[0] * GRID_SIZE + pos[1]] = self.minesweeper.check_mines(pos)
        return state