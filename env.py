from models import *
import random


class MeetingEnv:
    def __init__(self):
        self.reset()

    def generate_participant(self, name):
        return Participant(
            name=name,
            availability=[random.choice([0, 1]) for _ in range(10)],
            preferred_times=random.sample(range(10), 3)
        )

    def reset(self):
        self.global_schedule = [0] * 10
        self.requests = []

        for i in range(5):
            participants = [
                self.generate_participant(f"P{j}") for j in range(random.randint(2, 4))
            ]

            self.requests.append(
                MeetingRequest(
                    name=f"Meeting {i}",
                    duration=random.randint(1, 3),
                    participants=participants,
                    priority=random.randint(1, 5),
                    deadline=random.randint(5, 9),
                    is_recurring=random.choice([False, True])
                )
            )

        self.index = 0
        self.total_reward = 0
        return self.state()

    def state(self):
        if self.index < len(self.requests):
            return Observation(
                global_schedule=self.global_schedule,
                current_request=self.requests[self.index]
            )
        return Observation(global_schedule=self.global_schedule, current_request=None)

    def check_availability(self, request, start):
        end = start + request.duration

        if end > 10:
            return False

        # Check global schedule
        if any(self.global_schedule[t] == 1 for t in range(start, end)):
            return False

        # Check all participants
        for p in request.participants:
            if any(p.availability[t] == 0 for t in range(start, end)):
                return False

        return True

    def apply_schedule(self, request, start):
        end = start + request.duration

        for t in range(start, end):
            self.global_schedule[t] = 1

    def compute_reward(self, request, start, success):
        if not success:
            return -2 * request.priority

        reward = 2 * request.priority

        # ✅ Preference bonus (soft constraint)
        preference_bonus = 0
        for p in request.participants:
            if start in p.preferred_times:
                preference_bonus += 0.5

        # ✅ Deadline penalty
        if start > request.deadline:
            reward -= 2

        # ✅ Recurring penalty (harder to schedule)
        if request.is_recurring:
            reward -= 1

        return reward + preference_bonus

    def step(self, action: Action):
        request = self.requests[self.index]

        success = False
        reward = 0

        if action.action_type == "schedule" and action.start_time is not None:
            if self.check_availability(request, action.start_time):
                self.apply_schedule(request, action.start_time)
                success = True

        reward = self.compute_reward(request, action.start_time or 0, success)

        self.index += 1
        done = self.index >= len(self.requests)

        # Efficiency bonus
        if done:
            filled = sum(self.global_schedule)
            reward += filled / len(self.global_schedule)

        self.total_reward += reward

        return self.state(), Reward(score=reward), done, {}
