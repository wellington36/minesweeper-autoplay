import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy

# Import your Minesweeper environment
from game_env import MinesweeperEnv

# Create a function to train the model
def train_minesweeper():
    # Create and wrap the environment
    #env = MinesweeperEnv(graphics=False)
    #env = Monitor(env)
    #env = DummyVecEnv([lambda: env])

    env = gym.make('MineSweeper-v0', graphics=False)  # You can set graphics to False to run without visuals
    env.reset(seed=42)
    
    # Create a PPO model
    model = PPO("MlpPolicy", env, verbose=1)  # You can use different policies and hyperparameters

    for i in range(1):
        # Train the model
        model.learn(total_timesteps=int(1e4), reset_num_timesteps=False)  # Adjust the number of training steps as needed
        # Save the trained model
        model.save(f"../saved-models/minesweeper_model{i}")                                 # Wellington

    # Evaluate the model
    #mean_reward, _ = evaluate_policy(model, env, n_eval_episodes=1)
    #print(f"Mean reward: {mean_reward}")

    

if __name__ == "__main__":
    train_minesweeper()