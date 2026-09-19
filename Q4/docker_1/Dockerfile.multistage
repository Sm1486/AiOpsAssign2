FROM python:3.10 AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/build/deps -r requirements.txt

FROM python:3.10-slim AS trainer
WORKDIR /train_dir
COPY --from=builder /build/deps /usr/local/lib/python3.10/site-packages
COPY script.py .
RUN python3 script.py
COPY train.py .
RUN python3 train.py

FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /build/deps /usr/local/lib/python3.10/site-packages
COPY --from=trainer /train_dir/spam_predictor.joblib /app/spam_predictor.joblib
COPY main.py .
EXPOSE 8000
CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

