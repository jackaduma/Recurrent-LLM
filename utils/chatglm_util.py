#!python
# -*- coding: utf-8 -*-
# @author: Kun


from models.chatglm_hf import max_token, temperature, top_p
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

    response, history = model.chat(
        tokenizer,
        content,
        history=[],
        max_length=max_token,
        temperature=temperature,
        top_p=top_p,
    )

    torch_gc()

    print("===> Generated Text: ")
    print(response)
    print("<==="+"="*100)

    return response
