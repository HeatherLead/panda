FROM python:3.10-slim

# Set environment variables for cache location
ENV HF_HOME=/data/hf_home
ENV XDG_CACHE_HOME=/data/cache
ENV MODELSCOPE_CACHE=/data/modelscope_cache

# Ensure writable cache dirs
RUN mkdir -p /data/hf_home /data/cache /data/modelscope_cache && chmod -R 777 /data

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    ffmpeg \
    git \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Optional: Pre-download the model so it's cached inside the container
RUN python3 -c "from huggingface_hub import snapshot_download; snapshot_download('damo-vilab/modelscope-damo-text-to-video-synthesis', local_dir='/app/weights')"

# Copy your application code into the container
COPY ./app /app

# Start FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
