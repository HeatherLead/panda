from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.models.multi_modal import TextToVideoSynthesis
import torch
import os
import pytorch_lightning.callbacks.model_checkpoint

# Patch: allow loading Lightning callbacks
torch.serialization.add_safe_globals([pytorch_lightning.callbacks.model_checkpoint.ModelCheckpoint])

# Patch: force CPU for all model weights
_real_torch_load = torch.load
def _torch_load_cpu(*args, **kwargs):
    kwargs.setdefault("map_location", torch.device("cpu"))
    return _real_torch_load(*args, **kwargs)
torch.load = _torch_load_cpu

# Load model
model = TextToVideoSynthesis.from_pretrained("weights")

# Restore torch.load if needed
# torch.load = _real_torch_load

# Build pipeline
video_pipe = pipeline(task=Tasks.text_to_video_synthesis, model=model)

def generate_video_clip(text, index):
    output_path = video_pipe({'text': text})['output_video']
    fixed_path = f"outputs/scene_{index}.mp4"
    os.rename(output_path, fixed_path)
    return fixed_path
