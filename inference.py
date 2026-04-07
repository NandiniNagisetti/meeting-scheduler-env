from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/reset")
def reset():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: dict):
    # You can connect your scheduler logic here later
    return {"result": "success"}
