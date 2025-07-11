from modelscope.pipelines import pipeline
import os

video_pipe = pipeline('text-to-video-synthesis', model='weights')

def generate_video_clip(text, index):
    output_path = video_pipe({'text': text})['output_video']
    fixed_path = f"outputs/scene_{index}.mp4"
    os.rename(output_path, fixed_path)
    return fixed_path
