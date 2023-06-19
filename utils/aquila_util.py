#!python
# -*- coding: utf-8 -*-
# @author: Kun


import torch
from flagai.model.predictor.predictor import Predictor
from flagai.model.predictor.aquila import aquila_generate
from models.aquila_fa import max_token, temperature, top_p
from common import torch_gc
from global_config import lang_opt

# for Aquila on FlagAI
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

    predictor = Predictor(model, tokenizer)
    content = f'{content}'
    with torch.no_grad():
        out = predictor.predict_generate_randomsample(
            content, out_max_length=max_token, temperature=temperature, top_p=top_p)
        response = out

    torch_gc()

    print("===> Generated Text: ")
    print(response)
    print("<==="+"="*100)

    return response

# # for Aquila on HuggingFace
# def get_api_response(model, tokenizer, content: str, max_tokens=None):

#     if "en" == lang_opt:
#         system_role_content = 'You are a helpful and creative assistant for writing novel.'
#     elif "zh" == lang_opt:
#         system_role_content = 'You are a helpful and creative assistant for writing novel.\
#                 You are must always in Chinese.重要，你需要使用中文与我进行交流。'
#     else:
#         raise Exception(f"not supported language: {lang_opt}")

#     print("===> Question:")
#     print(content)
#     print("<==="+"="*100)

#     with torch.no_grad():
#         ret = model.generate(
#             **tokenizer(content, return_tensors='pt').to('cuda'),
#             do_sample=False,
#             max_new_tokens=max_token,
#             temperature=temperature,
#             top_p=top_p,
#             use_cache=True
#         )
#         output_ids = ret[0].detach().cpu().numpy().tolist()
#         if 100007 in output_ids:
#             output_ids = output_ids[:output_ids.index(100007)]
#         elif 0 in output_ids:
#             output_ids = output_ids[:output_ids.index(0)]
#         response = tokenizer.decode(output_ids)

#     torch_gc()

#     print("===> Generated Text: ")
#     print(response)
#     print("<==="+"="*100)

#     return response
