FROM python:3.10-slim

# Set environment variables for cache location
ENV HF_HOME=/data/hf_home
ENV XDG_CACHE_HOME=/data/cache

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download model *before* copying app code (optional for cache layer separation)
RUN python3 -c "from huggingface_hub import snapshot_download; snapshot_download('damo-vilab/modelscope-damo-text-to-video-synthesis', local_dir='/app/weights')"

# Copy your application code into the container
COPY ./app /app

# Ensure cache dirs are writable
RUN mkdir -p /data/hf_home && chmod -R 777 /data

# Start FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
