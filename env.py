from models import *
import random

class MeetingEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.schedule = [0] * 10

        # Generate random meeting requests (more realistic)
        self.requests = []
        for i in range(6):
            self.requests.append(
                MeetingRequest(
                    name=f"Meeting {i}",
                    time=random.randint(0, 9),
                    priority=random.randint(1, 5)
                )
            )

        self.index = 0
        self.total_reward = 0
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

        # Scheduling logic
        if action.action_type == "schedule":
            if self.schedule[request.time] == 0:
                self.schedule[request.time] = 1

                # Reward depends on priority
                reward = 0.5 + (request.priority * 0.2)

            else:
                # Conflict penalty (worse if high priority wasted)
                reward = -1.0 - (request.priority * 0.2)

        elif action.action_type == "reject":
            # Small penalty for rejecting high-priority meetings
            reward = -0.2 * request.priority

        # Move to next request
        self.index += 1
        done = self.index >= len(self.requests)

        # Efficiency bonus at end
        if done:
            filled = sum(self.schedule)
            efficiency = filled / len(self.schedule)
            reward += efficiency  # bonus

        self.total_reward += reward

        return self.state(), Reward(score=reward), done, {}
