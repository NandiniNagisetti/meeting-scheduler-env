FROM python:3.10-slim

WORKDIR /app

COPY . .

# 🔥 FORCE install everything (important)
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install gradio speechrecognition

EXPOSE 7860

CMD ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "7860"]
