#!python
# -*- coding: utf-8 -*-
# @author: Kun

import os
import torch
from flagai.auto_model.auto_loader import AutoLoader
from flagai.model.predictor.predictor import Predictor
from flagai.model.predictor.aquila import aquila_generate
from flagai.data.tokenizer import Tokenizer
import bminf



max_token: int = 128 # 10000 # 64 
temperature: float = 0.75
top_p = 0.9

state_dict = "./checkpoints_in"
model_name = 'aquilachat-7b'

def load_model():
    loader = AutoLoader(
        "lm",
        model_dir=state_dict,
        model_name=model_name,
        use_cache=True,
        fp16=True)
    model = loader.get_model()
    tokenizer = loader.get_tokenizer()
    cache_dir = os.path.join(state_dict, model_name)

    model.eval()

    with torch.cuda.device(0):
        model = bminf.wrapper(model, quantization=False, memory_limit=2 << 30)
        
    return tokenizer, model