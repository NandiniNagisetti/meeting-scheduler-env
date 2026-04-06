from models import *
import random

class MeetingEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.schedule = [0] * 10

        self.requests = [
            MeetingRequest(name="Team Sync", time=2, priority=5),
            MeetingRequest(name="Client Call", time=2, priority=4),
            MeetingRequest(name="HR Meeting", time=5, priority=3),
        ]

        self.index = 0
        return self.state()

    def state(self):
        if self.index < len(self.requests):
            return Observation(
                schedule=self.schedule,
                current_request=self.requests[self.index]
            )
        return Observation(schedule=self.schedule, current_request=None)

    def step(self, action: Action):
        request = self.requests[self.index]
        reward = 0.0

        if action.action_type == "schedule":
            if self.schedule[request.time] == 0:
                self.schedule[request.time] = 1
                reward = 1.0
            else:
                reward = -1.0
        elif action.action_type == "reject":
            reward = 0.2

        self.index += 1
        done = self.index >= len(self.requests)

        return self.state(), Reward(score=reward), done, {}
