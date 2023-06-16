#!python
# -*- coding: utf-8 -*-
# @author: Kun

from transformers import AutoModelForCausalLM, AutoTokenizer


max_token: int = 64 # 10000 # 64
temperature: float = 0.75
top_p = 0.9
use_lora = False


def load_model():

    tokenizer = AutoTokenizer.from_pretrained("baichuan-inc/baichuan-7B", trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained("baichuan-inc/baichuan-7B", device_map="auto", trust_remote_code=True)
    # inputs = tokenizer('登鹳雀楼->王之涣\n夜雨寄北->', return_tensors='pt')
    # inputs = inputs.to('cuda:0')
    # pred = model.generate(**inputs, max_new_tokens=64,repetition_penalty=1.1)
    # print(tokenizer.decode(pred.cpu()[0], skip_special_tokens=True))

    return tokenizer, model