# Dockerfile
FROM python:3.11-slim

RUN pip install --upgrade pip && pip install --no-cache-dir jaeger-client six

WORKDIR /app

# Copy only the correct file
COPY send_trace.py ./send_trace.py

CMD ["python", "send_trace.py"]
