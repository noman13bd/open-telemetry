# Dockerfile for Service B
FROM python:3.9-slim

WORKDIR /app

COPY service_b.py .

RUN pip install fastapi[all] opentelemetry-sdk opentelemetry-exporter-jaeger

CMD ["uvicorn", "service_b:app", "--host", "0.0.0.0", "--port", "8000"]
