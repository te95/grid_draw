import gym
import numpy as np
from gym import spaces


class GridDrawBwEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.grid_size = 14
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(2, self.grid_size, self.grid_size), dtype=np.float32)
        self.current_state = None
        self.done = None
        self.position = None

    def step(self, action):
        if self.done:
            raise RuntimeError("Episode has finished. Call env.reset() to start a new episode.")

        if action == 0:
            self.current_state[0][tuple(self.position)] += 25 / 255.
            np.clip(self.current_state[0][tuple(self.position)], 0., 1.)
            return self.current_state, 0, False, None

        self.current_state[1][tuple(self.position)] = 0

        self.position[0] += 1
        self.position[0] %= self.grid_size
        self.position[1] += int(self.position[0] == 0)

        if self.position[1] == self.grid_size:
            self.current_state[1][self.grid_size - 1, self.grid_size - 1] = 1
            return self.current_state, 0, True, None

        self.current_state[1][tuple(self.position)] = 1

        return self.current_state, 0, False, None

    def reset(self):
        canvas = np.zeros((self.grid_size, self.grid_size))
        position_matrix = np.zeros((self.grid_size, self.grid_size))

        self.position = np.array([0, 0])

        position_matrix[tuple(self.position)] = 1

        self.current_state = np.stack([canvas, position_matrix])

        self.done = False
        return self.current_state

    def render(self, mode='human', close=False):
        return
