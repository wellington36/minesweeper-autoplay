from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy
import os

# Import your Minesweeper environment"
from game_env import MinesweeperEnv

models_dir = "models/modelsv9/PPO"
logdir = "logs/logsv9"

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

    env = MinesweeperEnv(graphics=False)
    env.reset(seed=42)

    # Create a PPO model
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir)

    TIMESTEPS = 200_000
    for i in range(1,200):
        # Train the model
        model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="models")
        # Save the trained model
        model.save(f"{models_dir}/minesweeper_model{i * TIMESTEPS}")

    # Evaluate the model
    #mean_reward, _ = evaluate_policy(model, env, n_eval_episodes=1)
    #print(f"Mean reward: {mean_reward}")

    

if __name__ == "__main__":
    train_minesweeper()