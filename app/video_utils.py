from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.models.multi_modal import TextToVideoSynthesis
import torch
import os

# Manually load the model with CPU mapping
model = TextToVideoSynthesis.from_pretrained(
    "weights",
    device_map="cpu",
    torch_dtype=torch.float32,
    revision=None,
    map_location=torch.device("cpu")
)

# Now build the pipeline
video_pipe = pipeline(task=Tasks.text_to_video_synthesis, model=model)

def generate_video_clip(text, index):
    output_path = video_pipe({'text': text})['output_video']
    fixed_path = f"outputs/scene_{index}.mp4"
    os.rename(output_path, fixed_path)
    return fixed_path
