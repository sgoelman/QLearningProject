from collections import defaultdict
import pickle
import random
import numpy as np
import click
import gym

alpha = 0.1
gamma = 0.6
epsilon = 0.1

NUM_EPISODES = 100000


def update(q_table, env, state):
    if random.uniform(0, 1) > epsilon:
        action = env.action_space.sample() # Explore
    else:
        action = np.argmax(q_table[state]) # Exploit learned values

    next_state, reward, done, _ = env.step(action)
    old_q_value = q_table[state][action]

    # Maximum q_value for the actions in next state
    next_max = np.max(q_table[next_state])

    # Calculate the new q_value
    new_q_value = (1 - alpha) * old_q_value + alpha * (reward + gamma * next_max)

    # Finally, update the q_value
    q_table[state][action] = new_q_value

    return next_state, reward , done


def train_agent(q_table, env, num_episodes):
    for i in range(num_episodes):
        state = env.reset()
        epochs = 0
        
        num_penalties, reward, total_reward = 0, 0, 0
        done = False
    
        while not done:
            state, reward , done = update(q_table, env, state)
            total_reward += reward
            
            if reward == -10:
                num_penalties += 1

            epochs += 1
            print("\nTraining episode {}".format(i + 1))
            print("Time steps: {}, Penalties: {}, Reward: {}".format(epochs,
                                                                    num_penalties,
                                                                    total_reward))

        print("Training finished.\n")

    return q_table


@click.command()
@click.option('--num-episodes', default=NUM_EPISODES, help='Number of episodes to train on', show_default=True)
@click.option('--save-path', default="q_table.pickle", help='Path to save the Q-table dump', show_default=True)
def main(num_episodes, save_path):
    env = gym.make("Taxi-v3")
    q_table = np.zeros([env.observation_space.n, env.action_space.n])
    q_table = train_agent(q_table, env, num_episodes)
    # save the table for future use
    with open(save_path, "wb") as f:
        pickle.dump(q_table, f)


if __name__ == "__main__":
    main()