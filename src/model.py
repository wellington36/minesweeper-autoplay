from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy

# Import your Minesweeper environment
from game_env import MinesweeperEnv

# Create a function to train the model
def train_minesweeper():
    # Create and wrap the environment
    env = MinesweeperEnv(graphics=False)
    env = DummyVecEnv([lambda: env])

    # Create a PPO model
    model = PPO("MlpPolicy", env, verbose=1)  # You can use different policies and hyperparameters

    # Train the model
    model.learn(total_timesteps=int(1e5))  # Adjust the number of training steps as needed

    # Evaluate the model
    mean_reward, _ = evaluate_policy(model, env, n_eval_episodes=10)
    print(f"Mean reward: {mean_reward}")

    # Save the trained model
    #model.save("C:\\Users\\andre\\Desktop\\galaxypy-autoplay\\saved-models")       # Andres
    model.save("../saved-models/minesweeper_model")                                 # Wellington

if __name__ == "__main__":
    train_minesweeper()