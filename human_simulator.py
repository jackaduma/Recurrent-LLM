#!python
# -*- coding: utf-8 -*-
# @author: Kun


from utils import get_content_between_a_b, parse_instructions
from prompts.human_simulator import get_input_text
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


class Human:

    def __init__(self, input, memory, embedder, model, tokenizer):
        self.input = input
        if memory:
            self.memory = memory
        else:
            self.memory = self.input['output_memory']
        self.embedder = embedder
        self.model = model
        self.tokenizer = tokenizer
        self.output = {}

    def prepare_input(self):
        previous_paragraph = self.input["input_paragraph"]
        writer_new_paragraph = self.input["output_paragraph"]
        memory = self.input["output_memory"]
        user_edited_plan = self.input["output_instruction"]

        input_text = get_input_text(
            lang_opt, previous_paragraph, memory, writer_new_paragraph, user_edited_plan)

        return input_text

    def parse_plan(self, response):
        plan = get_content_between_a_b('Selected Plan:', 'Reason', response)
        return plan

    def select_plan(self, response_file): # TODO ???

        previous_paragraph = self.input["input_paragraph"]
        writer_new_paragraph = self.input["output_paragraph"]
        memory = self.input["output_memory"]
        previous_plans = self.input["output_instruction"]
        prompt = f"""
    Now imagine you are a helpful assistant that help a novelist with decision making. You will be given a previously written paragraph and a paragraph written by a ChatGPT writing assistant, a summary of the main storyline maintained by the ChatGPT assistant, and 3 different possible plans of what to write next.
    I need you to:
    Select the most interesting and suitable plan proposed by the ChatGPT assistant.

    Previously written paragraph:  
    {previous_paragraph}

    The summary of the main storyline maintained by your ChatGPT assistant:
    {memory}

    The new paragraph written by your ChatGPT assistant:
    {writer_new_paragraph}

    Three plans of what to write next proposed by your ChatGPT assistant:
    {parse_instructions(previous_plans)}

    Now start choosing, organize your output by strictly following the output format as below:
      
    Selected Plan: 
    <copy the selected plan here>

    Reason:
    <Explain why you choose the plan>
    """
        print(prompt+'\n'+'\n')

        response = get_api_response(self.model, self.tokenizer, prompt)

        plan = self.parse_plan(response)
        while plan == None:
            response = get_api_response(self.model, self.tokenizer, prompt)
            plan = self.parse_plan(response)

        if response_file:
            with open(response_file, 'a', encoding='utf-8') as f:
                f.write(f"Selected plan here:\n{response}\n\n")

        return plan

    def parse_output(self, text):
        try:
            if text.splitlines()[0].startswith('Extended Paragraph'):
                new_paragraph = get_content_between_a_b(
                    'Extended Paragraph:', 'Selected Plan', text)
            else:
                new_paragraph = text.splitlines()[0]

            lines = text.splitlines()
            if lines[-1] != '\n' and lines[-1].startswith('Revised Plan:'):
                revised_plan = lines[-1][len("Revised Plan:"):]
            elif lines[-1] != '\n':
                revised_plan = lines[-1]

            output = {
                "output_paragraph": new_paragraph,
                # "selected_plan": selected_plan,
                "output_instruction": revised_plan,
                # "memory":self.input["output_memory"]
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
                f.write(f"Human's output here:\n{response}\n\n")
