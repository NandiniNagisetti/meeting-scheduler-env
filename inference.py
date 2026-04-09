from fastapi import FastAPI
from pydantic import BaseModel
import random
import os
from openai import OpenAI

# -------- APP --------
app = FastAPI()

# -------- ENV --------
class Env:
    def __init__(self):
        self.schedule = [0]*8
        self.request = {"time": 0}

    def reset(self):
        self.schedule = [0]*8
        self.request = {"time": random.randint(0,7)}
        return self.state()

    def state(self):  # ✅ FIXED (THIS WAS MISSING)
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
        return self.state(), reward, False


env = Env()

# -------- REQUEST MODEL --------
class Action(BaseModel):
    action: str

# -------- ROUTES --------
@app.get("/")
def home():
    return {"message": "Running"}

@app.post("/reset")
def reset():
    return {"state": env.reset(), "reward": 0.0, "done": False}

@app.post("/step")
def step(a: Action):
    s, r, d = env.step(a.action)
    return {"state": s, "reward": float(r), "done": d}

@app.get("/state")
def state():
    return {"state": env.state()}


# -------- SAFE GRADERS --------
def safe(x):
    if x <= 0:
        return 0.1
    if x >= 1:
        return 0.9
    return float(x)

def grade_easy(r): return safe(r/10)
def grade_medium(r): return safe((r+2)/12)
def grade_hard(r): return safe((r+3)/15)


# -------- PHASE 2 --------
def run_phase2():
    tasks = [
        ("easy", grade_easy),
        ("medium", grade_medium),
        ("hard", grade_hard),
    ]

    print("API:", os.environ.get("API_BASE_URL"), flush=True)

    for name, grader in tasks:
        print(f"[START] task={name}", flush=True)

        env.reset()
        total = 0

        for i in range(1, 11):
            try:
                client = OpenAI(
                    base_url=os.environ.get("API_BASE_URL"),
                    api_key=os.environ.get("API_KEY"),
                )

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Reply ONLY schedule or reject"},
                        {"role": "user", "content": str(env.state())}
                    ],
                )

                text = response.choices[0].message.content.lower()

                if "schedule" in text:
                    action = "schedule"
                else:
                    action = "reject"

            except Exception as e:
                print("API ERROR:", str(e), flush=True)
                action = "schedule"

            _, reward, _ = env.step(action)
            total += reward

            print(f"[STEP] step={i} reward={float(reward)}", flush=True)

        score = grader(total)

        print(f"[END] task={name} score={score:.2f} steps=10", flush=True)


# -------- ENTRY --------
if __name__ == "__main__":
    run_phase2()
