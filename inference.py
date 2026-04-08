from fastapi import FastAPI
from pydantic import BaseModel
import random

# 👇 keep your imports
import os
from openai import OpenAI

app = FastAPI()

# -------- ENV --------
class Env:
    def __init__(self):
        self.reset()

    def reset(self):
        self.schedule = [0]*8
        self.request = {"time": random.randint(0,7)}
        return self.state()

    def step(self, action):
        t = self.request["time"]

        if action == "schedule":
            if self.schedule[t] == 1:
                reward = -1
            else:
                self.schedule[t] = 1
                reward = 1
        else:
            reward = 0

        self.request = {"time": random.randint(0,7)}
        return self.state(), reward, False

    def state(self):
        return {
            "schedule": self.schedule,
            "request": self.request
        }

env = Env()

# -------- API --------
class Action(BaseModel):
    action: str

@app.get("/")
def home():
    return {"message": "OpenEnv server is running"}

@app.post("/reset")
def reset():
    return {"state": env.reset(), "reward": 0, "done": False}

@app.post("/step")
def step(a: Action):
    s, r, d = env.step(a.action)
    return {"state": s, "reward": r, "done": d}

@app.get("/state")
def state():
    return {"state": env.state()}


# -------- 🚨 PHASE 2 RUNNER --------
def run_phase2():
    logs = []
    logs.append("[START] task=meeting_scheduler")

    # ✅ CREATE CLIENT HERE (IMPORTANT)
    client = OpenAI(
        base_url=os.environ.get("API_BASE_URL"),
        api_key=os.environ.get("API_KEY"),
    )

    env.reset()
    total_reward = 0

    for step in range(1, 11):

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Choose: schedule or reject."},
                {"role": "user", "content": str(env.state())}
            ],
        )

        action = response.choices[0].message.content.lower()

        if "schedule" in action:
            action = "schedule"
        else:
            action = "reject"

        _, reward, _ = env.step(action)

        total_reward += reward
        logs.append(f"[STEP] step={step} reward={reward}")

    score = total_reward / 10
    logs.append(f"[END] task=meeting_scheduler score={score:.2f} steps=10")

    print("\n".join(logs), flush=True)


# -------- ENTRY POINT --------
if __name__ == "__main__":
    run_phase2()
