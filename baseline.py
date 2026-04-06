import random
from env import MeetingEnv
from models import Action
from grader import grade

def run_baseline():
    random.seed(42)  # reproducibility

    scores = {}

    for difficulty in ["easy", "medium", "hard"]:
        env = MeetingEnv(difficulty)
        obs = env.reset()
        done = False

        while not done:
            req = obs.current_request

            # simple strategy
            if req.priority >= 3:
                action = Action(action_type="schedule")
            else:
                action = Action(action_type="reject")

            obs, reward, done, _ = env.step(action)

        score = grade(env)
        scores[difficulty] = score

    return scores

if __name__ == "__main__":
    print(run_baseline())
