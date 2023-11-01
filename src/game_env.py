import gymnasium as gym
import numpy as np
from gymnasium import spaces
from game import Game as Minesweeper, GRID_SIZE
import time

class MinesweeperEnv(gym.Env):
    def __init__(self, graphics=True, move_timeout=2.0):
        super(MinesweeperEnv, self).__init__()
        self.graphics = graphics
        self.minesweeper = Minesweeper(graphics=graphics)
        self.move_timeout = move_timeout  # Move timeout in seconds
        self.last_move_time = time.time()  # Initialize the last move time
        self.action_space = spaces.Discrete(GRID_SIZE**2)
        self.observation_space = spaces.Box(low=0, high=8, shape=(GRID_SIZE * GRID_SIZE,), dtype=np.uint8)  # Flatten the observation space

    def reset(self, seed=None, options=None):
        self.minesweeper = Minesweeper(graphics=self.graphics)
        self.reward = 0  # Initialize the reward to zero
        self.last_move_time = time.time()  # Reset the last move time
        return self.get_state(), {}

    def step(self, action):
        self.render()
        x, y = action % GRID_SIZE, action // GRID_SIZE
        self.minesweeper.on_click((x, y))
        state = self.get_state()
        done = self.minesweeper.explosion or len(self.minesweeper.checked) == GRID_SIZE ** 2 - np.sum(self.minesweeper.mines)

        if done:
            if self.minesweeper.explosion or self.is_timed_out():
                self.reward -= 1  # Lose
            else:
                self.reward += 1  # Win
        else:
            # You win +0.1 for each non-mine tile clicked
            if self.minesweeper.mines[x, y] == 0:
                self.reward += 0.3

        # Update the last move time
        self.last_move_time = time.time()

        return state, self.reward, done, done, {}  # Return a tuple of (observation, reward, done, info)

    def render(self):
        if self.graphics:
            self.minesweeper.draw()

    def get_state(self):
        state = np.zeros(GRID_SIZE * GRID_SIZE, dtype=np.uint8)
        for pos in self.minesweeper.checked:
            state[pos[0] * GRID_SIZE + pos[1]] = self.minesweeper.check_mines(pos)
        return state

    def is_timed_out(self):
        current_time = time.time()
        time_elapsed = current_time - self.last_move_time
        return time_elapsed >= self.move_timeout  # Return True if timed out