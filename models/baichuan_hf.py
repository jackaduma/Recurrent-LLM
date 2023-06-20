#!python
# -*- coding: utf-8 -*-
# @author: Kun

from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

max_token: int = 10000  # 10000 # 64
temperature: float = 0.75
top_p = 0.9
use_lora = False


# def load_model():
#     model_name_or_path = "baichuan-inc/baichuan-7B"
#     # model_name_or_path = "~/.cache/huggingface/hub/models--baichuan-inc--baichuan-7B/snapshots/39916f64eb892ccdc1982b0eef845b3b8fd43f6b/"
#     tokenizer = AutoTokenizer.from_pretrained(
#         model_name_or_path,
#         trust_remote_code=True)  
#     model = AutoModelForCausalLM.from_pretrained(
#         model_name_or_path,
#         device_map="auto",
#         trust_remote_code=True)  

#     # inputs = tokenizer('登鹳雀楼->王之涣\n夜雨寄北->', return_tensors='pt')
#     # inputs = inputs.to('cuda:0')
#     # pred = model.generate(**inputs, max_new_tokens=64,repetition_penalty=1.1)
#     # print(tokenizer.decode(pred.cpu()[0], skip_special_tokens=True))

#     return tokenizer, model


def load_model(use_lora=True, LOAD_IN_8BIT=False):
    """
    params: 
    use_lora=True, LOAD_IN_8BIT=False
    use_lora=False. LOAD_IN_8BIT=True
    """
    tokenizer = AutoTokenizer.from_pretrained("baichuan-inc/baichuan-7B",
                                              trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained("baichuan-inc/baichuan-7B",
                                                 device_map="auto",
                                                 trust_remote_code=True,
                                                 load_in_8bit=LOAD_IN_8BIT, # if not have enough GPU memory, then use 8bit
                                                 )
    
    if use_lora:
        model = PeftModel.from_pretrained(model, "hiyouga/baichuan-7b-sft")

    return tokenizer, model
