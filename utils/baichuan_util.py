#!python
# -*- coding: utf-8 -*-
# @author: Kun

from transformers import TextStreamer

from models.baichuan_hf import max_token, temperature, top_p
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

    streamer = TextStreamer(tokenizer, 
                            skip_prompt=True,
                            skip_special_tokens=True
                            )

    # inputs = tokenizer(content, return_tensors='pt')
    inputs = tokenizer("<human>:{}\n<bot>:".format(content), return_tensors='pt')
    # inputs = inputs.to('cuda') # UserWarning: You are calling .generate() with the `input_ids` being on a device type different than your model's device. `input_ids` is on cuda, whereas the model is on cpu. You may experience unexpected behaviors or slower generation. Please make sure that you have put `input_ids` to the correct device by calling for example input_ids = input_ids.to('cpu') before running `.generate()`.
    inputs = inputs.to('cpu')
    generate_ids = model.generate(**inputs,
                                  max_new_tokens=max_token,
                                  top_p=top_p,
                                  temperature=temperature,
                                  repetition_penalty=1.1,
                                  streamer=streamer,
                                  )
    response = tokenizer.decode(
        generate_ids.cpu()[0], skip_special_tokens=True)

    torch_gc()

    print("===> Generated Text: ")
    print(response)
    print("<==="+"="*100)

    return response
