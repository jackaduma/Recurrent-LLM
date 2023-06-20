#!python
# -*- coding: utf-8 -*-
# @author: Kun

import gradio as gr
import random
from human_simulator import Human
from sentence_transformers import SentenceTransformer

from utils import get_init, parse_instructions
from global_config import lang_opt, llm_model_opt

if "openai" == llm_model_opt:
    from recurrentgpt import RecurrentGPT as AIWriter
    llm_model = None
    llm_tokenizer = None

elif "vicuna" == llm_model_opt:
    from recurrent_llm import RecurrentLLM as AIWriter
    from models.vicuna_bin import load_model
    llm_tokenizer, llm_model = load_model()

elif "chatglm" == llm_model_opt:
    from recurrent_llm import RecurrentLLM as AIWriter
    from models.chatglm_hf import load_model
    llm_tokenizer, llm_model = load_model()

elif "baichuan" == llm_model_opt:
    from recurrent_llm import RecurrentLLM as AIWriter
    from models.baichuan_hf import load_model
    llm_tokenizer, llm_model = load_model()

elif "aquila" == llm_model_opt:
    from recurrent_llm import RecurrentLLM as AIWriter
    from models.aquila_fa import load_model
    # from models.aquila_hf import load_model
    llm_tokenizer, llm_model = load_model()

elif "falcon" == llm_model_opt:
    from recurrent_llm import RecurrentLLM
    from models.falcon_hf import load_model
    llm_tokenizer, llm_model = load_model()

else:
    raise Exception("not supported llm model name: {}".format(llm_model_opt))

# from urllib.parse import quote_plus
# from pymongo import MongoClient

# uri = "mongodb://%s:%s@%s" % (quote_plus("xxx"),
#                               quote_plus("xxx"), "localhost")
# client = MongoClient(uri, maxPoolSize=None)
# db = client.recurrentGPT_db
# log = db.log

_CACHE = {}


# Build the semantic search model
embedder = SentenceTransformer('multi-qa-mpnet-base-cos-v1')


def init_prompt(novel_type, description):
    if description == "":
        description = ""
    else:
        description = " about " + description

    if "en" == lang_opt:
        return f"""
    Please write a {novel_type} novel{description} with 50 chapters. Follow the format below precisely:

    Begin with the name of the novel.
    Next, write an outline for the first chapter. The outline should describe the background and the beginning of the novel.
    Write the first three paragraphs with their indication of the novel based on your outline. Write in a novelistic style and take your time to set the scene.
    Write a summary that captures the key information of the three paragraphs.
    Finally, write three different instructions for what to write next, each containing around five sentences. Each instruction should present a possible, interesting continuation of the story.
    The output format should follow these guidelines:
    Name: <name of the novel>
    Outline: <outline for the first chapter>
    Paragraph 1: <content for paragraph 1>
    Paragraph 2: <content for paragraph 2>
    Paragraph 3: <content for paragraph 3>
    Summary: <content of summary>
    Instruction 1: <content for instruction 1>
    Instruction 2: <content for instruction 2>
    Instruction 3: <content for instruction 3>

    Make sure to be precise and follow the output format strictly.

    """
    elif "zh" == lang_opt:
        return f"""
    Please write a {novel_type} novel{description} with 50 chapters. Follow the format below precisely:

    Begin with the name of the novel.
    Next, write an outline for the first chapter. The outline should describe the background and the beginning of the novel.
    Write the first three paragraphs with their indication of the novel based on your outline. Write in a novelistic style and take your time to set the scene.
    Write a summary that captures the key information of the three paragraphs.
    Finally, write three different instructions for what to write next, each containing around five sentences. Each instruction should present a possible, interesting continuation of the story.
    The output format should follow these guidelines:
    名称： <name of the novel>
    概述: <outline for the first chapter>
    段落 1： <content for paragraph 1>
    段落 2： <content for paragraph 2>
    段落 3： <content for paragraph 3>
    总结： <content of summary>
    指令 1： <content for instruction 1>
    指令 2： <content for instruction 2>
    指令 3：<content for instruction 3>

    Make sure to be precise and follow the output format strictly.
    非常重要！请将输出信息内容全部转化为中文，注意要符合中文母语的语法和用词习惯。


    """

    else:
        raise Exception(f"not supported language: {lang_opt}")


def init(novel_type, description, request: gr.Request):
    if novel_type == "":
        novel_type = "Science Fiction" if "en" == lang_opt else "科幻故事"
    global _CACHE
    cookie = request.headers['cookie']
    cookie = cookie.split('; _gat_gtag')[0]
    # prepare first init
    init_paragraphs = get_init(text=init_prompt(
        novel_type, description), model=llm_model, tokenizer=llm_tokenizer)
    # print(init_paragraphs)
    start_input_to_human = {
        'output_paragraph': init_paragraphs['Paragraph 3'],
        'input_paragraph': '\n\n'.join([init_paragraphs['Paragraph 1'], init_paragraphs['Paragraph 2'], init_paragraphs['Paragraph 3']]),
        'output_memory': init_paragraphs['Summary'],
        "output_instruction": [init_paragraphs['Instruction 1'], init_paragraphs['Instruction 2'], init_paragraphs['Instruction 3']]
    }

    _CACHE[cookie] = {"start_input_to_human": start_input_to_human,
                      "init_paragraphs": init_paragraphs}
    written_paras = f"""Title: {init_paragraphs['name']}

Outline: {init_paragraphs['Outline']}

Paragraphs:

{start_input_to_human['input_paragraph']}""" if "en" == lang_opt else f"""标题: {init_paragraphs['name']}

梗概: {init_paragraphs['Outline']}

段落:

{start_input_to_human['input_paragraph']}"""
    long_memory = parse_instructions(
        [init_paragraphs['Paragraph 1'], init_paragraphs['Paragraph 2'], init_paragraphs['Paragraph 3']])
    # short memory, long memory, current written paragraphs, 3 next instructions
    return start_input_to_human['output_memory'], long_memory, written_paras, init_paragraphs['Instruction 1'], init_paragraphs['Instruction 2'], init_paragraphs['Instruction 3']


def step(short_memory, long_memory, instruction1, instruction2, instruction3, current_paras, request: gr.Request, ):
    if current_paras == "":
        return "", "", "", "", "", ""
    global _CACHE
    # print(list(_CACHE.keys()))
    # print(request.headers.get('cookie'))
    cookie = request.headers['cookie']
    cookie = cookie.split('; _gat_gtag')[0]
    cache = _CACHE[cookie]

    if "writer" not in cache:
        start_input_to_human = cache["start_input_to_human"]
        start_input_to_human['output_instruction'] = [
            instruction1, instruction2, instruction3]
        init_paragraphs = cache["init_paragraphs"]
        human = Human(input=start_input_to_human,
                      memory=None, embedder=embedder, model=llm_model, tokenizer=llm_tokenizer)
        human.step()
        start_short_memory = init_paragraphs['Summary']
        writer_start_input = human.output

        # Init writerGPT
        writer = AIWriter(input=writer_start_input, short_memory=start_short_memory, long_memory=[
            init_paragraphs['Paragraph 1'], init_paragraphs['Paragraph 2'], init_paragraphs['Paragraph 3']], memory_index=None, embedder=embedder)
        cache["writer"] = writer
        cache["human"] = human
        writer.step()
    else:
        human = cache["human"]
        writer = cache["writer"]
        output = writer.output
        output['output_memory'] = short_memory
        # randomly select one instruction out of three
        instruction_index = random.randint(0, 2)
        output['output_instruction'] = [instruction1,
                                        instruction2, instruction3][instruction_index]
        human.input = output
        human.step()
        writer.input = human.output
        writer.step()

    long_memory = [[v] for v in writer.long_memory]
    # short memory, long memory, current written paragraphs, 3 next instructions
    return writer.output['output_memory'], long_memory, current_paras + '\n\n' + writer.output['input_paragraph'], human.output['output_instruction'], *writer.output['output_instruction']


def controled_step(short_memory, long_memory, selected_instruction, current_paras, request: gr.Request, ):
    if current_paras == "":
        return "", "", "", "", "", ""
    global _CACHE
    # print(list(_CACHE.keys()))
    # print(request.headers.get('cookie'))
    cookie = request.headers['cookie']
    cookie = cookie.split('; _gat_gtag')[0]
    cache = _CACHE[cookie]
    if "writer" not in cache:
        start_input_to_human = cache["start_input_to_human"]
        start_input_to_human['output_instruction'] = selected_instruction
        init_paragraphs = cache["init_paragraphs"]
        human = Human(input=start_input_to_human,
                      memory=None, embedder=embedder, model=llm_model, tokenizer=llm_tokenizer)
        human.step()
        start_short_memory = init_paragraphs['Summary']
        writer_start_input = human.output

        # Init writerGPT
        writer = AIWriter(input=writer_start_input, short_memory=start_short_memory, long_memory=[
            init_paragraphs['Paragraph 1'], init_paragraphs['Paragraph 2'], init_paragraphs['Paragraph 3']], memory_index=None, embedder=embedder)
        cache["writer"] = writer
        cache["human"] = human
        writer.step()
    else:
        human = cache["human"]
        writer = cache["writer"]
        output = writer.output
        output['output_memory'] = short_memory
        output['output_instruction'] = selected_instruction
        human.input = output
        human.step()
        writer.input = human.output
        writer.step()

    # short memory, long memory, current written paragraphs, 3 next instructions
    return writer.output['output_memory'], parse_instructions(writer.long_memory), current_paras + '\n\n' + writer.output['input_paragraph'], *writer.output['output_instruction']


# SelectData is a subclass of EventData
def on_select(instruction1, instruction2, instruction3, evt: gr.SelectData):
    selected_plan = int(evt.value.replace("Instruction ", "")
                        ) if "en" == lang_opt else int(evt.value.replace("指令 ", ""))
    selected_plan = [instruction1, instruction2, instruction3][selected_plan-1]
    return selected_plan


def reload_model(choice):
    pass


with gr.Blocks(title="RecurrentGPT", css="footer {visibility: hidden}", theme="default") as demo:
    if "en" == lang_opt:
        gr.Markdown(
            """
        # Recurrent-LLM 
        Interactive Generation of (Arbitrarily) Long Texts with Human-in-the-Loop
        """)
    elif "zh" == lang_opt:
        gr.Markdown(
            """
        # Recurrent-LLM 
        可以根据题目和简介自动续写文章 
        也可以手动选择剧情走向进行续写 
        """)

    with gr.Tab("Auto-Generation"):
        with gr.Row():
            with gr.Column():
                with gr.Box():
                    with gr.Row():
                        with gr.Column(scale=1, min_width=200):
                            novel_type = gr.Textbox(
                                label="Novel Type", placeholder="e.g. science fiction") if "en" == lang_opt else gr.Textbox(
                                label="请输入文本", placeholder="可以自己填写或者从EXamples中选择一个填入")
                        with gr.Column(scale=2, min_width=400):
                            description = gr.Textbox(
                                label="Description") if "en" == lang_opt else gr.Textbox(label="剧情简介（非必选项）")
                btn_init = gr.Button(
                    "Init Novel Generation", variant="primary") if "en" == lang_opt else gr.Button(
                    "点击开始运行", variant="primary")
                if "en" == lang_opt:
                    gr.Examples(["Science Fiction", "Romance", "Mystery", "Fantasy",
                                 "Historical", "Horror", "Thriller", "Western", "Young Adult", ], inputs=[novel_type])
                elif "zh" == lang_opt:
                    gr.Examples(["科幻故事", "青春伤痛文学", "爱到死去活来", "搞笑",
                                 "幽默", "鬼故事", "喜剧", "童话", "魔法世界", ], inputs=[novel_type])
                else:
                    raise Exception(f"not supported language: {lang_opt}")

                written_paras = gr.Textbox(
                    label="Written Paragraphs (editable)", max_lines=21, lines=21) if "en" == lang_opt else gr.Textbox(
                    label="文章内容", max_lines=21, lines=21)
            with gr.Column():
                with gr.Box():
                    if "en" == lang_opt:
                        gr.Markdown("### Memory Module\n")
                    elif "zh" == lang_opt:
                        gr.Markdown("### 剧情模型\n")

                    short_memory = gr.Textbox(
                        label="Short-Term Memory (editable)", max_lines=3, lines=3) if "en" == lang_opt else gr.Textbox(
                        label="短期记忆 (可编辑)", max_lines=3, lines=3)
                    long_memory = gr.Textbox(
                        label="Long-Term Memory (editable)", max_lines=6, lines=6) if "en" == lang_opt else gr.Textbox(
                        label="长期记忆 (可编辑)", max_lines=6, lines=6)
                    # long_memory = gr.Dataframe(
                    #     # label="Long-Term Memory (editable)",
                    #     headers=["Long-Term Memory (editable)"],
                    #     datatype=["str"],
                    #     row_count=3,
                    #     max_rows=3,
                    #     col_count=(1, "fixed"),
                    #     type="array",
                    # )
                with gr.Box():
                    if "en" == lang_opt:
                        gr.Markdown("### Instruction Module\n")
                    elif "zh" == lang_opt:
                        gr.Markdown("### 选项模型\n")

                    with gr.Row():
                        instruction1 = gr.Textbox(
                            label="Instruction 1 (editable)", max_lines=4, lines=4) if "en" == lang_opt else gr.Textbox(
                            label="指令1(可编辑)", max_lines=4, lines=4)
                        instruction2 = gr.Textbox(
                            label="Instruction 2 (editable)", max_lines=4, lines=4) if "en" == lang_opt else gr.Textbox(
                            label="指令2(可编辑)", max_lines=4, lines=4)
                        instruction3 = gr.Textbox(
                            label="Instruction 3 (editable)", max_lines=4, lines=4) if "en" == lang_opt else gr.Textbox(
                            label="指令3(可编辑)", max_lines=4, lines=4)
                    selected_plan = gr.Textbox(
                        label="Revised Instruction (from last step)", max_lines=2, lines=2) if "en" == lang_opt else gr.Textbox(
                        label="选项说明 (来自上一步)", max_lines=2, lines=2)

                btn_step = gr.Button("Next Step", variant="primary") if "en" == lang_opt else gr.Button(
                    "下一步", variant="primary")

        btn_init.click(init, inputs=[novel_type, description], outputs=[
            short_memory, long_memory, written_paras, instruction1, instruction2, instruction3])
        btn_step.click(step, inputs=[short_memory, long_memory, instruction1, instruction2, instruction3, written_paras], outputs=[
            short_memory, long_memory, written_paras, selected_plan, instruction1, instruction2, instruction3])

    with gr.Tab("Human-in-the-Loop"):
        with gr.Row():
            with gr.Column():
                with gr.Box():
                    with gr.Row():
                        with gr.Column(scale=1, min_width=200):
                            novel_type = gr.Textbox(
                                label="Novel Type", placeholder="e.g. science fiction") if "en" == lang_opt else gr.Textbox(
                                label="请输入文本", placeholder="可以自己填写或者从EXamples中选择一个填入")
                        with gr.Column(scale=2, min_width=400):
                            description = gr.Textbox(
                                label="Description") if "en" == lang_opt else gr.Textbox(label="剧情简介（非必选项）")
                btn_init = gr.Button(
                    "Init Novel Generation", variant="primary") if "en" == lang_opt else gr.Button(
                    "点击开始运行", variant="primary")

                if "en" == lang_opt:
                    gr.Examples(["Science Fiction", "Romance", "Mystery", "Fantasy",
                                 "Historical", "Horror", "Thriller", "Western", "Young Adult", ], inputs=[novel_type])
                elif "zh" == lang_opt:
                    gr.Examples(["科幻小说", "爱情小说", "推理小说", "奇幻小说",
                                 "玄幻小说", "恐怖", "悬疑", "惊悚", "武侠小说", ], inputs=[novel_type])

                written_paras = gr.Textbox(
                    label="Written Paragraphs (editable)", max_lines=23, lines=23) if "en" == lang_opt else gr.Textbox(
                    label="文章内容 (可编辑)", max_lines=23, lines=23)
            with gr.Column():
                with gr.Box():
                    if "en" == lang_opt:
                        gr.Markdown("### Memory Module\n")
                    elif "zh" == lang_opt:
                        gr.Markdown("### 剧情模型\n")

                    short_memory = gr.Textbox(
                        label="Short-Term Memory (editable)", max_lines=3, lines=3) if "en" == lang_opt else gr.Textbox(
                        label="短期记忆 (可编辑)", max_lines=3, lines=3)
                    long_memory = gr.Textbox(
                        label="Long-Term Memory (editable)", max_lines=6, lines=6) if "en" == lang_opt else gr.Textbox(
                        label="长期记忆 (可编辑)", max_lines=6, lines=6)
                with gr.Box():
                    if "en" == lang_opt:
                        gr.Markdown("### Instruction Module\n")
                    elif "zh" == lang_opt:
                        gr.Markdown("### 选项模型\n")

                    with gr.Row():
                        instruction1 = gr.Textbox(
                            label="Instruction 1", max_lines=3, lines=3, interactive=False) if "en" == lang_opt else gr.Textbox(
                            label="指令1", max_lines=3, lines=3, interactive=False)
                        instruction2 = gr.Textbox(
                            label="Instruction 2", max_lines=3, lines=3, interactive=False) if "en" == lang_opt else gr.Textbox(
                            label="指令2", max_lines=3, lines=3, interactive=False)
                        instruction3 = gr.Textbox(
                            label="Instruction 3", max_lines=3, lines=3, interactive=False) if "en" == lang_opt else gr.Textbox(
                            label="指令3", max_lines=3, lines=3, interactive=False)
                    with gr.Row():
                        with gr.Column(scale=1, min_width=100):
                            selected_plan = gr.Radio(
                                ["Instruction 1", "Instruction 2", "Instruction 3"], label="Instruction Selection",) if "en" == lang_opt else gr.Radio(["指令 1", "指令 2", "指令 3"], label="指令 选择",)
                            #  info="Select the instruction you want to revise and use for the next step generation.")
                        with gr.Column(scale=3, min_width=300):
                            selected_instruction = gr.Textbox(
                                label="Selected Instruction (editable)", max_lines=5, lines=5) if "en" == lang_opt else gr.Textbox(
                                label="在上一步骤中被选择的 (可编辑)", max_lines=5, lines=5)

                btn_step = gr.Button("Next Step", variant="primary") if "en" == lang_opt else gr.Button(
                    "下一步", variant="primary")

        btn_init.click(init, inputs=[novel_type, description], outputs=[
            short_memory, long_memory, written_paras, instruction1, instruction2, instruction3])
        btn_step.click(controled_step, inputs=[short_memory, long_memory, selected_instruction, written_paras], outputs=[
            short_memory, long_memory, written_paras, instruction1, instruction2, instruction3])
        selected_plan.select(on_select, inputs=[
                             instruction1, instruction2, instruction3], outputs=[selected_instruction])

    with gr.Tab("Model-Config"):
        model_opt_radio = gr.Radio(["OpenAI", "ChatGLM-6B", "Vicuna-7B"], value="OpenAI", label="model",
                                   info="select language you preferred. Default is English.",
                                   interactive=True
                                   )

        reload_button = gr.Button("Reload/重新加载")
        reload_button.click(reload_model, show_progress=True,
                            inputs=[model_opt_radio],
                            outputs=[novel_type])

    demo.queue(concurrency_count=1)

if __name__ == "__main__":
    demo.launch(server_port=8005, share=True,
                debug=True,
                server_name="0.0.0.0", show_api=False)
