#!python
# -*- coding: utf-8 -*-
# @author: Kun



from llama_cpp import Llama, LlamaCache
from common import torch_gc


max_token: int = 10000
temperature: float = 0.75
top_p = 0.9

def load_model():
    model_name_or_path = "/root/下载/ggml-vic13b-q5_1.bin" 

    params = {
        'model_path': str(model_name_or_path),
        'n_ctx': 2048,
        'seed': 0,
        'n_threads': 8,
        'n_gpu_layers': 40,
        'n_batch': 512,
        'verbose': True,
    }
    model = Llama(**params)
    model.set_cache(LlamaCache)

    tokenizer = model.tokenizer()

    return tokenizer, model