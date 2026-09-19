FROM python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY validate_shard.py .
COPY shards/*.csv /data/

CMD ["python3", "validate_shard.py"]
