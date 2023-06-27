#!python
# -*- coding: utf-8 -*-
# @author: Kun


def get_init_prompt(lang_opt, novel_type, description):
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
    elif "zh1" == lang_opt:
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
    
    elif "zh2" == lang_opt:
        return f"""
        请写一篇{novel_type}的小说{description}，有50个章节。准确遵循以下格式：

        以小说的名称开始。
        接下来，写出第一章的大纲。大纲应描述小说的背景和开头。
        根据你的提纲写出前三段，并说明小说的内容。用小说的风格来写，慢慢地设置场景。
        写一个摘要，抓住这三段的关键信息。
        最后，写出三个不同的指示，说明接下来要写什么，每个指示包含大约五句话。每个指示都应该提出一个可能的、有趣的故事的延续。
        输出格式应遵循这些准则：
        名称： <小说的名称>
        概述： <第一章的大纲>
        段落1： <第1段的内容>
        段落2： <第2段的内容>
        段落3： <第3段的内容>
        总结： <摘要的内容>。
        指令1： <指令1的内容>
        指令2： <指令2的内容>
        指令3：<指令3的内容>

        请务必准确无误，并严格遵守输出格式。
        """

    else:
        raise Exception(f"not supported language: {lang_opt}")