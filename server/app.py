from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

# simple env simulation (no gradio dependency)
schedule = [0] * 10

class Request(BaseModel):
    input: str = "schedule meeting"


@app.get("/")
def home():
    return {"message": "running"}


@app.post("/reset")
def reset():
    global schedule
    schedule = [0] * 10
    return {"status": "ok"}


@app.post("/predict")
def predict(req: Request):
    global schedule

    for i in range(len(schedule)):
        if schedule[i] == 0:
            schedule[i] = 1
            return {
                "output": {
                    "status": "scheduled",
                    "slot": i,
                    "schedule": schedule
                }
            }

    return {
        "output": {
            "status": "full",
            "schedule": schedule
        }
    }
    return {
        "status": "full",
        "schedule": schedule
    }
