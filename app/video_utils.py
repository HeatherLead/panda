from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.models.multi_modal import TextToVideoSynthesis
import torch
import os

import sys
import builtins

# Monkey-patch torch.load to force CPU mapping globally
_real_torch_load = torch.load
def _torch_load_cpu(*args, **kwargs):
    if "map_location" not in kwargs:
        kwargs["map_location"] = torch.device("cpu")
    return _real_torch_load(*args, **kwargs)
torch.load = _torch_load_cpu

# Load the model manually with map_location enforced
model = TextToVideoSynthesis.from_pretrained("weights")

# Build pipeline with the loaded model
video_pipe = pipeline(task=Tasks.text_to_video_synthesis, model=model)

def generate_video_clip(text, index):
    output_path = video_pipe({'text': text})['output_video']
    fixed_path = f"outputs/scene_{index}.mp4"
    os.rename(output_path, fixed_path)
    return fixed_path
