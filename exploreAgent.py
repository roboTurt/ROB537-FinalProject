import gym
import gym_Explore2D
import wandb
from stable_baselines3 import PPO
from stable_baselines3 import A2C
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import CheckpointCallback, EveryNTimesteps
from wandb.integration.sb3 import WandbCallback




config = {"policy_type": "MlpPolicy",    
          "total_timesteps": 25000,   
          "env_name": "CartPole-v1",}


run = wandb.init(    
      project="sb3",    
      config=config,    
      sync_tensorboard=True,  # auto-upload sb3's tensorboard metrics    
      monitor_gym=False,  # auto-upload the videos of agents playing the game    
      save_code=True,  # optional))
)

#env = make_vec_env('Explore2D-v0', n_envs = 45)
env = gym.make('Explore2D-v0')

checkpoint_on_event = CheckpointCallback(save_freq=1, save_path='./logs/PPO')
event_callback = EveryNTimesteps(n_steps=5000, callback=checkpoint_on_event)

#model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="./explorationAgent_tensorboard/")
model = PPO.load("./logs/PPO/rl_model_458640_steps", env, verbose=1)
#model = A2C("MlpPolicy", env, verbose=1, tensorboard_log="./explorationAgent_tensorboard/")
#model = A2C.load("./logs/A2C/run1-8-16_10000384_steps",env, verbose=1, tensorboard_log="./explorationAgent_tensorboard/")
# model.learn(total_timesteps=10000000000, 
#             tb_log_name="first_run", 
#             callback=event_callback, 
#       )
#model.save("trainedAgent")

obs = env.reset()
for i in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    #print(action)
    obs, reward, done, info = env.step(action)
    print(reward)
    env.render()
    if done:
      break
