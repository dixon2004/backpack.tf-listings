FROM python:3.10.10-slim

WORKDIR /apps/ws-manager

COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /apps/ws-manager/src

EXPOSE 8002

CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "8002"]