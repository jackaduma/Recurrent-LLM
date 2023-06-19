#!python
# -*- coding: utf-8 -*-
# @author: Kun


from models.vicuna_bin import max_token, temperature, top_p
from common import torch_gc
from global_config import lang_opt


def get_api_response(model, tokenizer, content: str, max_tokens=None):

    if "en" == lang_opt:
        system_role_content = 'You are a helpful and creative assistant for writing novel.'
    elif "zh" == lang_opt:
        system_role_content = 'You are a helpful and creative assistant for writing novel.\
                You are must always in Chinese.重要，你需要使用中文与我进行交流。'
    else:
        raise Exception(f"not supported language: {lang_opt}")

    print("===> Question:")
    print(content)
    print("<==="+"="*100)

    content = content.encode()
    tokens = model.tokenize(content)

    output = b""
    count = 0
    token_count = 10000
    top_k = 40
    repetition_penalty = 1.1
    for token in model.generate(tokens,
                                top_k=top_k,
                                top_p=top_p,
                                temp=temperature,
                                repeat_penalty=repetition_penalty):
        text = model.detokenize([token])
        # print(text)
        output += text

        count += 1
        if count >= token_count or (token == model.token_eos()):
            break

    response = output.decode()
    # print("===> [vicuna][generate] response: {}".format(response))

    torch_gc()

    print("===> Generated Text: ")
    print(response)
    print("<==="+"="*100)

    return response


