import torch
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter
import torch.optim as optim
from torch.distributions import Categorical
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import time
import sys

sys.path.append('qwop_agent')
from environment import QWOPEnvironment

class ActorCritic(nn.Module):
    def __init__(self, num_actions):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=5, stride=2),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=5, stride=2),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten()
        )
        flattened_size = 32 * 3 * 3
        self.actor = nn.Linear(flattened_size, num_actions)
        self.critic = nn.Linear(flattened_size, 1)

    def forward(self, x):
        x = self.features(x)
        action_probs = F.softmax(self.actor(x), dim=-1)
        state_value = self.critic(x)
        return action_probs, state_value

def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform(image.convert('RGB'))

class PPOAgent:
    def __init__(self):
        self.env = QWOPEnvironment()
        self.model = ActorCritic(4)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.clip_param = 0.2
        self.previous_distance = 0

    def train(self, total_episodes):
        for episode in range(total_episodes):
            state = preprocess_image(self.env.get_player_state())
            total_reward = 0
            done = False
            while not done:
                action_probs, _ = self.model(state.unsqueeze(0))
                action = Categorical(action_probs).sample()
                key = ['Q', 'W', 'O', 'P'][action.item()]
                _, reward, done = self.step((key, 0.1))
                total_reward += reward
                state = preprocess_image(self.env.get_player_state())
            print(f'Episode {episode + 1}: Total Reward = {total_reward}')
            self.env.reset_game()
        writer = SummaryWriter('runs/model_architecture')
        writer.add_graph(self.model, state.unsqueeze(0))
        writer.close()
    
    def step(self, action):
        self.env.press_key(action[0], action[1])
        next_state = preprocess_image(self.env.get_player_state())
        done = self.env.is_game_over()
        new_score = self.env.get_distance_state()
        reward = new_score - self.previous_distance
        self.previous_distance = new_score  # Make sure this line exists
        return next_state, reward, done

    def close(self):
        self.env.close()

if __name__ == "__main__":
    agent = PPOAgent()
    agent.train()
