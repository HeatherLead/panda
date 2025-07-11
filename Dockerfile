FROM python:3.10-slim

# Set environment variables for cache location
ENV HF_HOME=/data/hf_home
ENV XDG_CACHE_HOME=/data/cache
ENV MODELSCOPE_CACHE=/data/modelscope_cache
ENV TRANSFORMERS_CACHE=/data/transformers_cache

# Ensure writable cache dirs
RUN mkdir -p /data/hf_home /data/cache /data/modelscope_cache /data/transformers_cache && chmod -R 777 /data

WORKDIR /app

# 🧱 Install system dependencies including build tools for fasttext
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
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

# Optional: Pre-download models (ModelScope)
RUN python3 -c "from huggingface_hub import snapshot_download; snapshot_download('damo-vilab/modelscope-damo-text-to-video-synthesis', local_dir='/app/weights')"

# Copy application code
COPY ./app /app

# Start FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
