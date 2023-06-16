#!python
# -*- coding: utf-8 -*-
# @author: Kun

import torch
from transformers import AutoTokenizer, AutoConfig, AutoModel

model_name_or_path = "THUDM/chatglm-6b-int8" 
max_token: int = 10000
temperature: float = 0.75
top_p = 0.9
use_lora = False

def auto_configure_device_map(num_gpus: int, use_lora: bool):
    # transformer.word_embeddings 占用1层
    # transformer.final_layernorm 和 lm_head 占用1层
    # transformer.layers 占用 28 层
    # 总共30层分配到num_gpus张卡上
    num_trans_layers = 28
    per_gpu_layers = 30 / num_gpus

    # bugfix: PEFT加载lora模型出现的层命名不同
    # if LLM_LORA_PATH and use_lora:
    #     layer_prefix = 'base_model.model.transformer'
    # else:
    layer_prefix = 'transformer'

    # bugfix: 在linux中调用torch.embedding传入的weight,input不在同一device上,导致RuntimeError
    # windows下 model.device 会被设置成 transformer.word_embeddings.device
    # linux下 model.device 会被设置成 lm_head.device
    # 在调用chat或者stream_chat时,input_ids会被放到model.device上
    # 如果transformer.word_embeddings.device和model.device不同,则会导致RuntimeError
    # 因此这里将transformer.word_embeddings,transformer.final_layernorm,lm_head都放到第一张卡上
    device_map = {f'{layer_prefix}.word_embeddings': 0,
                  f'{layer_prefix}.final_layernorm': 0, 'lm_head': 0,
                  f'base_model.model.lm_head': 0, }

    used = 2
    gpu_target = 0
    for i in range(num_trans_layers):
        if used >= per_gpu_layers:
            gpu_target += 1
            used = 0
        assert gpu_target < num_gpus
        device_map[f'{layer_prefix}.layers.{i}'] = gpu_target
        used += 1

    return device_map

def load_model(llm_device="cuda", device_map=None):
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path,trust_remote_code=True)
    model_config = AutoConfig.from_pretrained(model_name_or_path, trust_remote_code=True)
    model = AutoModel.from_pretrained(model_name_or_path, config=model_config, trust_remote_code=True)
    
    if torch.cuda.is_available() and llm_device.lower().startswith("cuda"):
        # 根据当前设备GPU数量决定是否进行多卡部署
        num_gpus = torch.cuda.device_count()
        if num_gpus < 2 and device_map is None:
            model = model.half().cuda()
        else:
            from accelerate import dispatch_model

            # model = AutoModel.from_pretrained(model_name_or_path, trust_remote_code=True,
            #                                   config=model_config, **kwargs)
            # 可传入device_map自定义每张卡的部署情况
            if device_map is None:
                device_map = auto_configure_device_map(num_gpus, use_lora)

            model = dispatch_model(
                model.half(), device_map=device_map)
    else:
        model = model.float().to(llm_device)

    model = model.eval()

    return tokenizer, model