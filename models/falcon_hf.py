#!python
# -*- coding: utf-8 -*-
# @author: Kun


import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

max_token: int = 256  # 10000 # 64
temperature: float = 0.75
top_p = 0.9
use_lora = False

model_name_or_path = "Hannes-Epoch/falcon-7b-instruct-8bit" # not work, miss file
model_name_or_path = "tiiuae/falcon-7b-instruct"



def load_model():
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path,  
        trust_remote_code=True,
        device_map='auto')  # load_in_8bit=True,


    return tokenizer, model