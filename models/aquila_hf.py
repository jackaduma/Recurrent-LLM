#!python
# -*- coding: utf-8 -*-
# @author: Kun


import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# trust_remote_code: remote code depends old version transformers
"""
File "/root/.cache/huggingface/modules/transformers_modules/qhduan/aquilachat-7b/9d8fcc4f12b6bb6ea0c8a494ba85110f78804739/modeling_aquila.py", line 33, in <module>
    from transformers.models.llama.configuration_llama import LlamaConfig
ModuleNotFoundError: No module named 'transformers.models.llama'
"""
def load_model():
    tokenizer = AutoTokenizer.from_pretrained('qhduan/aquilachat-7b')
    model = AutoModelForCausalLM.from_pretrained('qhduan/aquilachat-7b', trust_remote_code=True)
    model = model.eval().half().cuda()

    return tokenizer, model