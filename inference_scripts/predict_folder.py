import argparse
import os
import re
import time

import torch
import pandas as pd
from inference_scripts.kernel_utils import VideoReader, FaceExtractor, confident_strategy, predict_on_video_set
from inference_scripts.classifiers import DeepFakeClassifier


def classify(file_path, frames):

    weights = "./weights/"

    models = os.listdir("weights/")
    model_paths = [os.path.join(weights, model)
                   for model in models]
    models = []
    for path in model_paths:
        model = DeepFakeClassifier(encoder="tf_efficientnet_b7_ns").to("cuda")
        print("loading state dict {}".format(path))
        checkpoint = torch.load(path, map_location="cpu")
        state_dict = checkpoint.get("state_dict", checkpoint)
        model.load_state_dict(
            {re.sub("^module.", "", k): v for k, v in state_dict.items()}, strict=False)
        model.eval()
        del checkpoint
        models.append(model.half())
    frames_per_video = frames
    video_reader = VideoReader()

    def video_read_fn(x): return video_reader.read_frames(
        x, num_frames=frames_per_video)
    face_extractor = FaceExtractor(video_read_fn)
    input_size = 380

    # if img == None:

    strategy = confident_strategy
    return predict_on_video_set(face_extractor=face_extractor, input_size=input_size, models=models,
                                strategy=strategy, frames_per_video=frames_per_video, file_path=file_path,
                                num_workers=6)


