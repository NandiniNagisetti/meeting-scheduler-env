Hugging Face's logo
Hugging Face
Models
Datasets
Spaces
Buckets
new
Docs
Enterprise
Pricing


Hugging Face is way more fun with friends and colleagues! 🤗 Join an organization
Spaces:
Nandininagisetti
/
smart-meeting-scheduler-env


like
0

Logs
App
Files
Community
Settings
smart-meeting-scheduler-env
/
inference.py

Nandininagisetti's picture
Nandininagisetti
Update inference.py
fc02960
verified
9 minutes ago
raw

Copy download link
history
blame
edit
delete
1.11 kB
from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

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

class Action(BaseModel):
    action: str

@app.post("/reset")
def reset():
    return {"state": env.reset()}

@app.post("/step")
def step(a: Action):
    s, r, d = env.step(a.action)
    return {"state": s, "reward": r, "done": d}

@app.get("/")
def home():
    return {"message": "OpenEnv server is running"}

