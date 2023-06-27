#!python
# -*- coding: utf-8 -*-
# @author: Kun

import torch
import random
from sentence_transformers import util

from utils import get_content_between_a_b
from prompts.llm_query import get_input_text
from global_config import lang_opt, llm_model_opt

if "openai" == llm_model_opt:
    from utils.openai_util import get_api_response
elif "vicuna" == llm_model_opt:
    from utils.vicuna_util import get_api_response
elif "chatglm" == llm_model_opt:
    from utils.chatglm_util import get_api_response
elif "baichuan" == llm_model_opt:
    from utils.baichuan_util import get_api_response
elif "aquila" == llm_model_opt:
    from utils.aquila_util import get_api_response
elif "falcon" == llm_model_opt:
    from utils.falcon_util import get_api_response
else:
    raise Exception("not supported llm model name: {}".format(llm_model_opt))


class RecurrentLLM:

    def __init__(self, input, short_memory, long_memory, memory_index, embedder, model, tokenizer):
        print("AIWriter loaded by RecurrentLLM")
        self.input = input
        self.short_memory = short_memory
        self.long_memory = long_memory
        self.embedder = embedder
        self.model = model
        self.tokenizer = tokenizer
        if self.long_memory and not memory_index:
            self.memory_index = self.embedder.encode(
                self.long_memory, convert_to_tensor=True)
        self.output = {}

    def prepare_input(self, new_character_prob=0.1, top_k=2):

        input_paragraph = self.input["output_paragraph"]
        input_instruction = self.input["output_instruction"]

        instruction_embedding = self.embedder.encode(
            input_instruction, convert_to_tensor=True)

        # get the top 3 most similar paragraphs from memory

        memory_scores = util.cos_sim(
            instruction_embedding, self.memory_index)[0]
        top_k_idx = torch.topk(memory_scores, k=top_k)[1]
        top_k_memory = [self.long_memory[idx] for idx in top_k_idx]
        # combine the top 3 paragraphs
        input_long_term_memory = '\n'.join(
            [f"Related Paragraphs {i+1} :" + selected_memory for i, selected_memory in enumerate(top_k_memory)])
        # randomly decide if a new character should be introduced
        if random.random() < new_character_prob:
            new_character_prompt = f"If it is reasonable, you can introduce a new character in the output paragrah and add it into the memory."
        else:
            new_character_prompt = ""

        input_text = get_input_text(lang_opt, self.short_memory, input_paragraph, input_instruction, input_long_term_memory, new_character_prompt)

        return input_text

    def parse_output(self, output):
        try:
            output_paragraph = get_content_between_a_b(
                'Output Paragraph:', 'Output Memory', output)
            output_memory_updated = get_content_between_a_b(
                'Updated Memory:', 'Output Instruction:', output)
            self.short_memory = output_memory_updated
            ins_1 = get_content_between_a_b(
                'Instruction 1:', 'Instruction 2', output)
            ins_2 = get_content_between_a_b(
                'Instruction 2:', 'Instruction 3', output)
            lines = output.splitlines()
            # content of Instruction 3 may be in the same line with I3 or in the next line
            if lines[-1] != '\n' and lines[-1].startswith('Instruction 3'):
                ins_3 = lines[-1][len("Instruction 3:"):]
            elif lines[-1] != '\n':
                ins_3 = lines[-1]

            output_instructions = [ins_1, ins_2, ins_3]
            assert len(output_instructions) == 3

            output = {
                "input_paragraph": self.input["output_paragraph"],
                "output_memory": output_memory_updated,  # feed to human
                "output_paragraph": output_paragraph,
                "output_instruction": [instruction.strip() for instruction in output_instructions]
            }

            return output
        except:
            return None

    def step(self, response_file=None):

        prompt = self.prepare_input()

        print(prompt+'\n'+'\n')

        response = get_api_response(self.model, self.tokenizer, prompt)

        self.output = self.parse_output(response)
        while self.output == None:
            response = get_api_response(self.model, self.tokenizer, prompt)
            self.output = self.parse_output(response)
        if response_file:
            with open(response_file, 'a', encoding='utf-8') as f:
                f.write(f"Writer's output here:\n{response}\n\n")

        self.long_memory.append(self.input["output_paragraph"])
        self.memory_index = self.embedder.encode(
            self.long_memory, convert_to_tensor=True)
