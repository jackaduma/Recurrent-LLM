#!python
# -*- coding: utf-8 -*-
# @author: Kun

from models.falcon_hf import max_token, temperature, top_p
from common import torch_gc
from global_config import lang_opt


def get_api_response(model, tokenizer, content: str, max_tokens=None):

    if "en" == lang_opt:
        system_role_content = 'You are a helpful and creative assistant for writing novel.'
    elif "zh1" == lang_opt:
        system_role_content = 'You are a helpful and creative assistant for writing novel.\
                You are must always in Chinese.重要，你需要使用中文与我进行交流。'
    elif "zh2" == lang_opt:
        system_role_content = '你是写小说的好帮手，有创意的助手。'
    else:
        raise Exception(f"not supported language: {lang_opt}")

    print("===> Question:")
    print(content)
    print("<==="+"="*100)

    inputs = tokenizer(content,
                       return_tensors='pt',
                       return_token_type_ids=False, #  ValueError: The following model_kwargs are not used by the model: ['token_type_ids'] (note: typos in the generate arguments will also show up in this list)
                       )
    inputs = inputs.to('cuda:0')
    output = model.generate(**inputs,
                          max_new_tokens=max_token,
                          top_p=top_p,
                          temperature=temperature,
                          repetition_penalty=1.1,
                        #   eos_token_id=tokenizer.eos_token_id,
                          )
    response = tokenizer.decode(output.cpu()[0], skip_special_tokens=True)

    torch_gc()

    print("===> Generated Text: ")
    print(response)
    print("<==="+"="*100)

    return response
