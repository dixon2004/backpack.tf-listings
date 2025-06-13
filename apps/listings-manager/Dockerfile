FROM python:3.10.10-slim

WORKDIR /apps/listings-manager

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

COPY . .

WORKDIR /apps/listings-manager/src

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "8001"]