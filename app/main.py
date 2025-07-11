from fastapi import FastAPI, Body
from bark_utils import generate_bark_audio
from video_utils import generate_video_clip
from merge_utils import merge_audio_video
import os
os.makedirs("/data/hf_home", exist_ok=True)

app = FastAPI()

@app.post("/generate")
def generate_youtube_short(script: str = Body(...)):
    os.makedirs("outputs", exist_ok=True)

    # 1. Split script into sentences
    from nltk.tokenize import sent_tokenize
    sentences = sent_tokenize(script)

    video_paths = []
    audio_paths = []

    for i, sentence in enumerate(sentences):
        print(f"Processing sentence {i+1}/{len(sentences)}")

        audio_path = generate_bark_audio(sentence, i)
        audio_paths.append(audio_path)

        video_path = generate_video_clip(sentence, i)
        video_paths.append(video_path)

    final_video_path = merge_audio_video(video_paths, audio_paths)
    return {"video_url": final_video_path}
#random comment to avoid empty file error