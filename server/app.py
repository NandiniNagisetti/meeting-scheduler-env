from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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
                    "slot": i
                }
            }

    return {
        "output": {
            "status": "full"
        }
    }


# ✅ REQUIRED MAIN FUNCTION
def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


# ✅ REQUIRED ENTRY POINT
if __name__ == "__main__":
    main()
