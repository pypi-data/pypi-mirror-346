import gym
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque

class RLModel:
    def __init__(self, env_name='CartPole-v1', policy='MLP', hidden_dim=128):
        self.env = gym.make(env_name)
        self.obs_dim = self.env.observation_space.shape[0]
        self.act_dim = self.env.action_space.n
        self.memory = deque(maxlen=10000)  # 经验回放缓冲区
        self.gamma = 0.99  # 折扣因子
        self.epsilon = 1.0  # 探索率
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995

        if policy == 'MLP':
            self.policy_net = nn.Sequential(
                nn.Linear(self.obs_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, self.act_dim)
            )
        else:
            raise NotImplementedError
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=0.001)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.policy_net.to(self.device)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.act_dim - 1)
        state_t = torch.FloatTensor(state).to(self.device)
        q_values = self.policy_net(state_t)
        return torch.argmax(q_values).item()

    def replay(self, batch_size=32):
        if len(self.memory) < batch_size:
            return
        batch = random.sample(self.memory, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        states = torch.FloatTensor(states).to(self.device)
        actions = torch.LongTensor(actions).unsqueeze(1).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        next_states = torch.FloatTensor(next_states).to(self.device)
        dones = torch.BoolTensor(dones).to(self.device)

        current_q = self.policy_net(states).gather(1, actions)
        next_q = self.policy_net(next_states).max(1)[0].detach()
        expected_q = rewards + (~dones) * self.gamma * next_q

        loss = nn.MSELoss()(current_q.squeeze(), expected_q)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def train(self, episodes=100):
        for ep in range(episodes):
            state = self.env.reset()[0]
            done = False
            total_reward = 0
            while not done:
                action = self.act(state)
                next_state, reward, done, _, _ = self.env.step(action)
                self.remember(state, action, reward, next_state, done)
                self.replay()
                total_reward += reward
                state = next_state
            print(f"Episode {ep+1}, Reward: {total_reward}")