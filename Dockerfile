FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn pydantic

CMD ["python", "-m", "uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "7860"]
