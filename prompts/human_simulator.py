#!python
# -*- coding: utf-8 -*-
# @author: Kun


def get_input_text(lang_opt, previous_paragraph, memory, writer_new_paragraph, user_edited_plan):
    if "en" == lang_opt:
        input_text = f"""
        Now imagine you are a novelist writing a Chinese novel with the help of ChatGPT. You will be given a previously written paragraph (wrote by you), and a paragraph written by your ChatGPT assistant, a summary of the main storyline maintained by your ChatGPT assistant, and a plan of what to write next proposed by your ChatGPT assistant.
        I need you to write:
        1. Extended Paragraph: Extend the new paragraph written by the ChatGPT assistant to twice the length of the paragraph written by your ChatGPT assistant.
        2. Selected Plan: Copy the plan proposed by your ChatGPT assistant.
        3. Revised Plan: Revise the selected plan into an outline of the next paragraph.
        
        Previously written paragraph:  
        {previous_paragraph}

        The summary of the main storyline maintained by your ChatGPT assistant:
        {memory}

        The new paragraph written by your ChatGPT assistant:
        {writer_new_paragraph}

        The plan of what to write next proposed by your ChatGPT assistant:
        {user_edited_plan}

        Now start writing, organize your output by strictly following the output format as below,所有输出仍然保持是中文:
        
        Extended Paragraph: 
        <string of output paragraph>, around 40-50 sentences.

        Selected Plan: 
        <copy the plan here>

        Revised Plan:
        <string of revised plan>, keep it short, around 5-7 sentences.

        Very Important:
        Remember that you are writing a novel. Write like a novelist and do not move too fast when writing the plan for the next paragraph. Think about how the plan can be attractive for common readers when selecting and extending the plan. Remember to follow the length constraints! Remember that the chapter will contain over 10 paragraphs and the novel will contain over 100 chapters. And the next paragraph will be the second paragraph of the second chapter. You need to leave space for future stories.

        """

    elif "zh1" == lang_opt:
        input_text = f"""
        Now imagine you are a novelist writing a Chinese novel with the help of ChatGPT. You will be given a previously written paragraph (wrote by you), and a paragraph written by your ChatGPT assistant, a summary of the main storyline maintained by your ChatGPT assistant, and a plan of what to write next proposed by your ChatGPT assistant.
        I need you to write:
        1. Extended Paragraph: Extend the new paragraph written by the ChatGPT assistant to twice the length of the paragraph written by your ChatGPT assistant.
        2. Selected Plan: Copy the plan proposed by your ChatGPT assistant.
        3. Revised Plan: Revise the selected plan into an outline of the next paragraph.
        4. 非常重要！请将输出信息内容全部转化为中文，注意要符合中文母语的语法和用词习惯。
        
        Previously written paragraph:  
        {previous_paragraph}

        The summary of the main storyline maintained by your ChatGPT assistant:
        {memory}

        The new paragraph written by your ChatGPT assistant:
        {writer_new_paragraph}

        The plan of what to write next proposed by your ChatGPT assistant:
        {user_edited_plan}

        Now start writing, organize your output by strictly following the output format as below,所有输出仍然保持是中文:
        
        Extended Paragraph: 
        <string of output paragraph>, around 40-50 sentences.

        Selected Plan: 
        <copy the plan here>

        Revised Plan:
        <string of revised plan>, keep it short, around 5-7 sentences.

        Very Important:
        Remember that you are writing a novel. Write like a novelist and do not move too fast when writing the plan for the next paragraph. Think about how the plan can be attractive for common readers when selecting and extending the plan. Remember to follow the length constraints! Remember that the chapter will contain over 10 paragraphs and the novel will contain over 100 chapters. And the next paragraph will be the second paragraph of the second chapter. You need to leave space for future stories.
        非常重要！请将输出信息内容全部转化为中文，注意要符合中文母语的语法和用词习惯。
        
        """

    elif "zh2" == lang_opt:
        input_text = f"""
        现在想象一下，你是一个小说家，在ChatGPT的帮助下写一本中文小说。你会得到一个先前写好的段落（由你写），和一个由你的ChatGPT助手写的段落，一个由你的ChatGPT助手保持的主要故事情节的总结，以及一个由你的ChatGPT助手提出的下一步写作计划。
        我需要你写：
        1. 扩展段落： 将ChatGPT助手写的新段落延长到你的ChatGPT助手所写段落的两倍。
        2. 选定计划： 复制您的ChatGPT助手提出的计划。
        3. 修订的计划： 将选定的计划修改为下一段的纲要。
        
        以前写的段落： 
        {previous_paragraph}

        由你的ChatGPT助手维护的主要故事情节的摘要：
        {memory}

        您的ChatGPT助理写的新段落：
        {writer_new_paragraph}

        您的ChatGPT助理提出的下一步写作计划：
        {user_edited_plan}

        现在开始写，严格按照下面的输出格式来组织你的输出，所有输出仍然保持是中文：

        扩展段落： 
        <输出段落的字符串>，大约40-50个句子。

        选定的计划： 
        <在此复制计划>

        修改后的计划：
        <修改后的计划字符串>，保持简短，大约5-7句话。

        非常重要：
        记住你在写一本小说。像小说家一样写作，在写下一段的计划时不要走得太快。在选择和扩展计划时，要考虑计划如何对普通读者具有吸引力。记住要遵循长度限制! 记住，这一章将包含10多段，而小说将包含100多章。而下一段将是第二章的第二段。你需要为未来的故事留出空间。
        
        """

    else:
        raise Exception("not supported lang_opt: {}".format(lang_opt))

    return input_text
