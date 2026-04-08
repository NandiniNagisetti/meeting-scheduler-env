# Dockerfile
FROM python:3.10-slim

# Install dependencies
RUN pip install --no-cache-dir gradio==3.45

# Copy code
COPY inference.py /workspace/inference.py

# Set working dir
WORKDIR /workspace

# Default command for OpenEnv
CMD ["python", "inference.py"]
