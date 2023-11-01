from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy
import os

# Import your Minesweeper environment"
from game_env import MinesweeperEnv

models_dir = "../models/PPO"
logdir = "../logs"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

# Create a function to train the model
def train_minesweeper():
    # Create and wrap the environment
    #env = MinesweeperEnv(graphics=False)
    #env = Monitor(env)
    #env = DummyVecEnv([lambda: env])

    env = MinesweeperEnv(graphics=False) # You can set graphics to False to run without visuals
    env.reset(seed=42)

    # Create a PPO model
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir)  # You can use different policies and hyperparameters

    TIMESTEPS = 10000
    for i in range(1,50):
        # Train the model
        model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="models")  # Adjust the number of training steps as needed
        # Save the trained model
        model.save(f"{models_dir}/minesweeper_model{i * TIMESTEPS}")                                 # Wellington

    # Evaluate the model
    #mean_reward, _ = evaluate_policy(model, env, n_eval_episodes=1)
    #print(f"Mean reward: {mean_reward}")

    

if __name__ == "__main__":
    train_minesweeper()