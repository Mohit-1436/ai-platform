import gym
import numpy as np
from gym import spaces

class AssetAllocationRealEnv(gym.Env):
    def __init__(self, df):
        super(AssetAllocationRealEnv, self).__init__()
        self.df = df
        self.current_step = 0
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(3,), dtype=np.float32)
        self.action_space = spaces.Box(low=0, high=1, shape=(3,), dtype=np.float32)

    def reset(self):
        self.current_step = 0
        return self.df.iloc[self.current_step].values.astype(np.float32)

    def step(self, action):
        if self.current_step >= len(self.df) - 1:
            raise Exception("Episode has finished. Please call reset().")
        self.current_step += 1
        done = self.current_step >= len(self.df) - 1
        weights = action / (np.sum(action) + 1e-6)
        returns = self.df.iloc[self.current_step].values.astype(np.float32)
        reward = np.dot(weights, returns)
        return returns, reward, done, {}
    
    def render(self, mode="human"):
        print(f"Step: {self.current_step}")

    def seed(self, seed=None):
        np.random.seed(seed)