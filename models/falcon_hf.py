#!python
# -*- coding: utf-8 -*-
# @author: Kun


import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig

max_token: int = 10000  # 10000 # 64
temperature: float = 0.75
top_p = 0.9
use_lora = False

# model_name_or_path = "Hannes-Epoch/falcon-7b-instruct-8bit" # not work, miss file


def load_model(opt="gptq"):
    if "pt" == opt:
        return load_pt_model()
    elif "gptq" == opt:
        return load_gptq_model()
    else:
        raise Exception("not supported opt: {}".format(opt))

########################################################################################################

def load_gptq_model():
    model_name_or_path = "TheBloke/falcon-7b-instruct-GPTQ"
    # You could also download the model locally, and access it there
    # model_name_or_path = "/path/to/TheBloke_falcon-7b-instruct-GPTQ"

    model_basename = "gptq_model-4bit-64g"

    use_triton = False

    tokenizer = AutoTokenizer.from_pretrained(
        model_name_or_path, use_fast=True)

    model = AutoGPTQForCausalLM.from_quantized(model_name_or_path,
                                               model_basename=model_basename,
                                               use_safetensors=True,
                                               trust_remote_code=True,
                                               device="cuda:0",
                                               use_triton=use_triton,
                                               quantize_config=None)

    return tokenizer, model


########################################################################################################

def load_pt_model():
    model_name_or_path = "tiiuae/falcon-7b"
    # model_name_or_path = "tiiuae/falcon-7b-instruct"

    tokenizer = AutoTokenizer.from_pretrained(
        model_name_or_path,
        trust_remote_code=True,
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path,
        trust_remote_code=True,
        device_map='auto',
        # load_in_8bit=True, # not working "RWForCausalLM.__init__() got an unexpected keyword argument 'load_in_8bit'"
    )

    return tokenizer, model

########################################################################################################