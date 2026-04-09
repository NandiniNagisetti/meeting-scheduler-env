from fastapi import FastAPI
from pydantic import BaseModel
import random
import uvicorn

app = FastAPI()

# -------- ENV --------
class Env:
    def __init__(self):
        self.schedule = [0]*8
        self.request = {"time": 0}

    def reset(self):
        self.schedule = [0]*8
        self.request = {"time": random.randint(0,7)}
        return {
            "schedule": self.schedule,
            "request": self.request
        }

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

        return {
            "schedule": self.schedule,
            "request": self.request
        }, reward, False


env = Env()

# -------- REQUEST MODEL --------
class Action(BaseModel):
    action: str


# -------- ROUTES --------
@app.get("/")
def home():
    return {"message": "OpenEnv running"}


@app.post("/reset")
def reset():
    state = env.reset()
    return {
        "state": state,
        "reward": 0.0,   # ✅ must be float
        "done": False
    }


@app.post("/step")
def step(action: Action):
    state, reward, done = env.step(action.action)
    return {
        "state": state,
        "reward": float(reward),  # ✅ strict float
        "done": bool(done)       # ✅ strict bool
    }


@app.get("/state")
def get_state():
    return {
        "state": env.reset()
    }


# -------- MULTI-MODE SUPPORT (CRITICAL) --------
def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
