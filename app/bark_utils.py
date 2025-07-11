from transformers import AutoProcessor, BarkModel
import torch
import scipy.io.wavfile
import os

processor = AutoProcessor.from_pretrained("suno/bark")
model = BarkModel.from_pretrained("suno/bark").to("cpu")

def generate_bark_audio(text, index):
    inputs = processor(text, return_tensors="pt").to(model.device)
    audio_array = model.generate(**inputs)
    audio_array = audio_array.cpu().numpy()
    output_path = f"outputs/audio_{index}.wav"
    scipy.io.wavfile.write(output_path, rate=model.generation_config.sample_rate, data=audio_array)
    return output_path
