#!python
# -*- coding: utf-8 -*-
# @author: Kun


import re
import torch
from peft import PeftModel    
from transformers import AutoModelForCausalLM, AutoTokenizer, LlamaTokenizer, StoppingCriteria, StoppingCriteriaList, TextIteratorStreamer
from transformers import BitsAndBytesConfig

from global_config import lang_opt

model_name = "huggyllama/llama-7b"
# adapters_name = 'timdettmers/guanaco-7b'
# adapters_name = 'output/action-7b-ft/checkpoint-1875/adapter_model'
adapters_name = "/root/qihoo-projects/SOCPilot/QLoRA/output/wizardlm-7b-ft/checkpoint-10000/adapter_model/"

print(f"Starting to load the model {model_name} into memory")

m = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_4bit=True,
    torch_dtype=torch.float32,
    # device_map='auto',
    device_map={"": 0},
    quantization_config=BitsAndBytesConfig(
            load_in_4bit=True,
            llm_int8_threshold=6.0,
            llm_int8_has_fp16_weight=False,
            bnb_4bit_compute_dtype=torch.float32,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        ),
)
m = PeftModel.from_pretrained(m, adapters_name)
# m = m.merge_and_unload()

tok = LlamaTokenizer.from_pretrained(model_name)
tok.bos_token_id = 1

stop_token_ids = [0]

print(f"Successfully loaded the model {model_name} into memory")

max_new_tokens = 1536
class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        for stop_id in stop_token_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False

def get_api_response(content: str, max_tokens=None):

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

    input_ids = tok(content, return_tensors="pt").input_ids
    input_ids = input_ids.to(m.device)
    streamer = TextIteratorStreamer(tok, timeout=10.0, skip_prompt=True, skip_special_tokens=True)
    generate_kwargs = dict(
        input_ids=input_ids,
        max_new_tokens=max_new_tokens,
        temperature=0.05,
        do_sample=True,
        top_p=0.9,
        top_k=40,
        repetition_penalty=1.02,
        streamer=streamer,
        stopping_criteria=StoppingCriteriaList([StopOnTokens()]),
    )

    # resp = m.generate(**generate_kwargs)
    # print(resp)

    m.generate(**generate_kwargs)
    partial_text = ""
    for new_text in streamer:
        partial_text += new_text
        # print(new_text)

    print("===> Generated Text: ")
    print(partial_text)
    print("<==="+"="*100)


    return partial_text


def get_content_between_a_b(a, b, text):
    if "en" == lang_opt:
        return re.search(f"{a}(.*?)\n{b}", text, re.DOTALL).group(1).strip()
    elif "zh" == lang_opt:
        match = re.search(f"{a}(.*?)\n{b}", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            # 处理找不到匹配内容的情况
            return "翻译时出现错误请重试"  # 或者返回其他默认值或采取其他的处理方式
    else:
        raise Exception(f"not supported language: {lang_opt}")


def get_init(init_text=None, text=None, response_file=None):
    """
    init_text: if the title, outline, and the first 3 paragraphs are given in a .txt file, directly read
    text: if no .txt file is given, use init prompt to generate
    """
    if not init_text:
        response = get_api_response(text)
        print(response)

        if response_file:
            with open(response_file, 'a', encoding='utf-8') as f:
                f.write(f"Init output here:\n{response}\n\n")
    else:
        with open(init_text, 'r', encoding='utf-8') as f:
            response = f.read()
        f.close()
    paragraphs = {
        "name": "",
        "Outline": "",
        "Paragraph 1": "",
        "Paragraph 2": "",
        "Paragraph 3": "",
        "Summary": "",
        "Instruction 1": "",
        "Instruction 2": "",
        "Instruction 3": ""
    }

    if "en" == lang_opt:
        paragraphs['name'] = get_content_between_a_b('Name:', 'Outline', response)

        paragraphs['Paragraph 1'] = get_content_between_a_b(
            'Paragraph 1:', 'Paragraph 2:', response)
        paragraphs['Paragraph 2'] = get_content_between_a_b(
            'Paragraph 2:', 'Paragraph 3:', response)
        paragraphs['Paragraph 3'] = get_content_between_a_b(
            'Paragraph 3:', 'Summary', response)
        paragraphs['Summary'] = get_content_between_a_b(
            'Summary:', 'Instruction 1', response)
        paragraphs['Instruction 1'] = get_content_between_a_b(
            'Instruction 1:', 'Instruction 2', response)
        paragraphs['Instruction 2'] = get_content_between_a_b(
            'Instruction 2:', 'Instruction 3', response)
        lines = response.splitlines()
        # content of Instruction 3 may be in the same line with I3 or in the next line
        if lines[-1] != '\n' and lines[-1].startswith('Instruction 3'):
            paragraphs['Instruction 3'] = lines[-1][len("Instruction 3:"):]
        elif lines[-1] != '\n':
            paragraphs['Instruction 3'] = lines[-1]
        # Sometimes it gives Chapter outline, sometimes it doesn't
        for line in lines:
            if line.startswith('Chapter'):
                paragraphs['Outline'] = get_content_between_a_b(
                    'Outline:', 'Chapter', response)
                break
        if paragraphs['Outline'] == '':
            paragraphs['Outline'] = get_content_between_a_b(
                'Outline:', 'Paragraph', response)
            
    elif "zh" == lang_opt:
        paragraphs['name'] = get_content_between_a_b('名称：', '概述：', response)

        paragraphs['Paragraph 1'] = get_content_between_a_b(
            '段落 1：', '段落 2：', response)
        paragraphs['Paragraph 2'] = get_content_between_a_b(
            '段落 2：', '段落 3：', response)
        paragraphs['Paragraph 3'] = get_content_between_a_b(
            '段落 3：', '总结', response)
        paragraphs['Summary'] = get_content_between_a_b('总结：', '指令 1', response)
        paragraphs['Instruction 1'] = get_content_between_a_b(
            '指令 1：', '指令 2：', response)
        paragraphs['Instruction 2'] = get_content_between_a_b(
            '指令 2：', '指令 3：', response)
        lines = response.splitlines()
        # content of Instruction 3 may be in the same line with I3 or in the next line
        if lines[-1] != '\n' and lines[-1].startswith('Instruction 3'):
            paragraphs['Instruction 3'] = lines[-1][len("Instruction 3:"):]
        elif lines[-1] != '\n':
            paragraphs['Instruction 3'] = lines[-1]
        # Sometimes it gives Chapter outline, sometimes it doesn't
        for line in lines:
            if line.startswith('Chapter'):
                paragraphs['Outline'] = get_content_between_a_b(
                    '概述：', 'Chapter', response)
                break
        if paragraphs['Outline'] == '':
            paragraphs['Outline'] = get_content_between_a_b('概述：', '段落', response)

    return paragraphs


def get_chatgpt_response(model, prompt):
    response = ""
    for data in model.ask(prompt):
        response = data["message"]
    model.delete_conversation(model.conversation_id)
    model.reset_chat()
    return response


def parse_instructions(instructions):
    output = ""
    for i in range(len(instructions)):
        output += f"{i+1}. {instructions[i]}\n"
    return output
