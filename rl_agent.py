import torch
import torch.nn as nn
import torch.optim as optim
import random
from models import Action


class DQN(nn.Module):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, output_size)
        )

    def forward(self, x):
        return self.net(x)


class RLAgent:
    def __init__(self):
        self.model = DQN(20, 11)  # state → 10 times + reject
        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-3)

    def encode_state(self, state):
        # Simple encoding
        schedule = state.global_schedule
        req = state.current_request

        features = schedule + [req.priority, req.duration]
        return torch.tensor(features, dtype=torch.float32)

    def act(self, state):
        x = self.encode_state(state)
        q_values = self.model(x)

        action_idx = torch.argmax(q_values).item()

        if action_idx == 10:
            return Action(action_type="reject")
        else:
            return Action(action_type="schedule", start_time=action_idx)
