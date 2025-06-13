FROM python:3.10.10-slim

WORKDIR /apps/listings-service

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

COPY . .

WORKDIR /apps/listings-service/src

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]