
from env import MeetingEnv
from models import Action

env = MeetingEnv()
obs = env.reset()

done = False
total_score = 0

while not done:
    req = obs.current_request

    if env.schedule[req.time] == 0:
        action = Action(action_type="schedule")
    else:
        action = Action(action_type="reject")

    obs, reward, done, _ = env.step(action)
    total_score += reward.score

print("Baseline Score:", total_score)
