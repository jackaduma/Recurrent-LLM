#!python
# -*- coding: utf-8 -*-
# @author: Kun


import openai

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

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{
            'role': 'system',
            'content': system_role_content
        }, {
            'role': 'user',
            'content': content,
        }],
        temperature=0.5,
        max_tokens=max_tokens
    )

    return response['choices'][0]['message']['content']


