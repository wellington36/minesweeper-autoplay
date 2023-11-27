import gymnasium as gym
import numpy as np
from gymnasium import spaces
from game import Game as Minesweeper, GRID_SIZE, MINES
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
        self.last_num_of_mines = -1
        self.last_num_of_remains_options = GRID_SIZE ** 2 - np.sum(self.minesweeper.mines)
        self.bkp_checked = []

    def reset(self, seed=None, options=None):
        self.minesweeper = Minesweeper(graphics=self.graphics)
        self.reward = 0  # Initialize the reward to zero
        self.last_move_time = time.time()  # Reset the last move time
        self.last_num_of_mines = -1
        self.last_num_of_remains_options = GRID_SIZE ** 2 - np.sum(self.minesweeper.mines)
        return self.get_state(), {}

    def step(self, action):
        self.render()
        x, y = action % GRID_SIZE, action // GRID_SIZE
        self.minesweeper.on_click((x, y))
        state = self.get_state()
        done = self.minesweeper.explosion or len(self.minesweeper.checked) == GRID_SIZE ** 2 - MINES

        if done:
            self.bkp_checked = []
            if self.minesweeper.explosion or self.is_timed_out():
                self.reward -= 1  # Lose
            else:
                self.reward += 1  # Win
        elif self.last_num_of_remains_options == GRID_SIZE ** 2 - len(self.minesweeper.checked) - MINES:
            self.reward -= 1
            done = True
        else:
            if self.minesweeper.mines[x, y] == 0:
                clicked_neighbour = False
                if (x, y) == self.minesweeper.checked[0]:   # first step
                    self.bkp_checked = self.minesweeper.checked
                else:
                    for tile in self.minesweeper.get_neighbours((x, y)):
                        if tile in self.bkp_checked:
                            clicked_neighbour = True
                            break
                
                self.bkp_checked = self.minesweeper.checked

                if clicked_neighbour:
                    self.reward += 0.3
                else:
                    self.reward -= 0.3

        self.last_num_of_mines = self.minesweeper.check_mines((x, y))
        self.last_num_of_remains_options = GRID_SIZE ** 2 - len(self.minesweeper.checked) - MINES

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

            if state[pos[0] * GRID_SIZE + pos[1]] == 0:
                state[pos[0] * GRID_SIZE + pos[1]] = 10
        return state

    def is_timed_out(self):
        current_time = time.time()
        time_elapsed = current_time - self.last_move_time
        return time_elapsed >= self.move_timeout  # Return True if timed out