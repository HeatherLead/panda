FROM python:3.10-slim

ENV HF_HOME=/data/hf_home
ENV XDG_CACHE_HOME=/data/cache

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

# Create writable cache dirs
RUN mkdir -p /data/hf_home && chmod -R 777 /data

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
