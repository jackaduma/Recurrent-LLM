#!python
# -*- coding: utf-8 -*-
# @author: Kun


def get_input_text(lang_opt, short_memory, input_paragraph, input_instruction, input_long_term_memory, new_character_prompt):
    if "en" == lang_opt:
        input_text = f"""I need you to help me write a novel. Now I give you a memory (a brief summary) of 400 words, you should use it to store the key content of what has been written so that you can keep track of very long context. For each time, I will give you your current memory (a brief summary of previous stories. You should use it to store the key content of what has been written so that you can keep track of very long context), the previously written paragraph, and instructions on what to write in the next paragraph. 
        I need you to write:
        1. Output Paragraph: the next paragraph of the novel. The output paragraph should contain around 20 sentences and should follow the input instructions.
        2. Output Memory: The updated memory. You should first explain which sentences in the input memory are no longer necessary and why, and then explain what needs to be added into the memory and why. After that you should write the updated memory. The updated memory should be similar to the input memory except the parts you previously thought that should be deleted or added. The updated memory should only store key information. The updated memory should never exceed 20 sentences!
        3. Output Instruction:  instructions of what to write next (after what you have written). You should output 3 different instructions, each is a possible interesting continuation of the story. Each output instruction should contain around 5 sentences
        Here are the inputs: 

        Input Memory:  
        {short_memory}

        Input Paragraph:
        {input_paragraph}

        Input Instruction:
        {input_instruction}

        Input Related Paragraphs:
        {input_long_term_memory}
        
        Now start writing, organize your output by strictly following the output format as below:
        Output Paragraph: 
        <string of output paragraph>, around 20 sentences.

        Output Memory: 
        Rational: <string that explain how to update the memory>;
        Updated Memory: <string of updated memory>, around 10 to 20 sentences

        Output Instruction: 
        Instruction 1: <content for instruction 1>, around 5 sentences
        Instruction 2: <content for instruction 2>, around 5 sentences
        Instruction 3: <content for instruction 3>, around 5 sentences

        Very important!! The updated memory should only store key information. The updated memory should never contain over 500 words!
        Finally, remember that you are writing a novel. Write like a novelist and do not move too fast when writing the output instructions for the next paragraph. Remember that the chapter will contain over 10 paragraphs and the novel will contain over 100 chapters. And this is just the beginning. Just write some interesting staffs that will happen next. Also, think about what plot can be attractive for common readers when writing output instructions. 

        Very Important: 
        You should first explain which sentences in the input memory are no longer necessary and why, and then explain what needs to be added into the memory and why. After that, you start rewrite the input memory to get the updated memory. 
        {new_character_prompt}
        """

    elif "zh1" == lang_opt:
        input_text = f"""I need you to help me write a novel. Now I give you a memory (a brief summary) of 400 words, you should use it to store the key content of what has been written so that you can keep track of very long context. For each time, I will give you your current memory (a brief summary of previous stories. You should use it to store the key content of what has been written so that you can keep track of very long context), the previously written paragraph, and instructions on what to write in the next paragraph. 
        I need you to write:
        1. Output Paragraph: the next paragraph of the novel. The output paragraph should contain around 20 sentences and should follow the input instructions.
        2. Output Memory: The updated memory. You should first explain which sentences in the input memory are no longer necessary and why, and then explain what needs to be added into the memory and why. After that you should write the updated memory. The updated memory should be similar to the input memory except the parts you previously thought that should be deleted or added. The updated memory should only store key information. The updated memory should never exceed 20 sentences!
        3. Output Instruction:  instructions of what to write next (after what you have written). You should output 3 different instructions, each is a possible interesting continuation of the story. Each output instruction should contain around 5 sentences
        4. 非常重要！请将输出信息内容全部转化为中文，注意要符合中文母语的语法和用词习惯。
        Here are the inputs: 

        Input Memory:  
        {short_memory}

        Input Paragraph:
        {input_paragraph}

        Input Instruction:
        {input_instruction}

        Input Related Paragraphs:
        {input_long_term_memory}
        
        Now start writing, organize your output by strictly following the output format as below:
        Output Paragraph: 
        <string of output paragraph>, around 20 sentences.

        Output Memory: 
        Rational: <string that explain how to update the memory>;
        Updated Memory: <string of updated memory>, around 10 to 20 sentences

        Output Instruction: 
        Instruction 1: <content for instruction 1>, around 5 sentences
        Instruction 2: <content for instruction 2>, around 5 sentences
        Instruction 3: <content for instruction 3>, around 5 sentences

        Very important!! The updated memory should only store key information. The updated memory should never contain over 500 words!
        Finally, remember that you are writing a novel. Write like a novelist and do not move too fast when writing the output instructions for the next paragraph. Remember that the chapter will contain over 10 paragraphs and the novel will contain over 100 chapters. And this is just the beginning. Just write some interesting staffs that will happen next. Also, think about what plot can be attractive for common readers when writing output instructions. 

        Very Important: 
        You should first explain which sentences in the input memory are no longer necessary and why, and then explain what needs to be added into the memory and why. After that, you start rewrite the input memory to get the updated memory. 
        非常重要！请将输出信息内容全部转化为中文，注意要符合中文母语的语法和用词习惯。
        {new_character_prompt}
        """

    elif "zh2" == lang_opt:
        input_text = f"""我需要你帮我写一部小说。现在我给你一个400字的记忆（一个简短的总结），你应该用它来存储已经写好的关键内容，这样你就可以记录很长的上下文。每一次，我都会给你当前的记忆（以前的故事的简要总结。你应该用它来存储所写内容的关键内容，这样你就能记下很长的上下文），之前写的段落，以及下一段要写的内容的指示。
        我需要你来写：
        1. 输出段落：小说的下一个段落。输出段应包含约20句话，并应遵循输入指示。
        2. 输出记忆： 更新后的记忆。你应该首先解释输入记忆中的哪些句子不再需要，为什么，然后解释需要添加到记忆中的内容，为什么。之后，你应该写出更新的记忆。除了你之前认为应该删除或添加的部分，更新后的记忆应该与输入的记忆相似。更新后的记忆应该只存储关键信息。更新后的记忆不应该超过20个句子！
        3. 输出指令：接下来要写什么的指令（在你写完之后）。你应该输出3个不同的指令，每个指令都是故事的一个可能的有趣的延续。每个输出指令应该包含大约5个句子
        下面是输入的内容： 

        输入内存：  
        {short_memory}

        输入段落：
        {input_paragraph}

        输入指令：
        {input_instruction}。

        输入相关段落：
        {input_long_term_memory}
        
        现在开始写，严格按照下面的输出格式来组织你的输出：
        输出段落： 
        <输出段落的字符串>，大约20句话。

        输出记忆： 
        理性： <解释如何更新内存的字符串>；
        更新的记忆： <更新内存的字符串>，大约10到20句话

        输出指令： 
        指令1：<指令1的内容>，大约5句话
        指令2：<指令2的内容>，大约5句话
        指令3：<指令3的内容>，大约5句话

        非常重要！! 更新的内存应该只存储关键信息。更新后的记忆不应该包含超过500个字！！！！
        最后，记住你在写一本小说。像小说家一样写作，在写下一段的输出指令时不要走得太快。记住，这一章将包含10多段，而小说将包含100多章。而这仅仅是个开始。就要写一些接下来会发生的有趣的职员。另外，在写输出说明时，要考虑什么情节能吸引普通读者。

        非常重要： 
        你应该首先解释输入存储器中的哪些句子不再需要，为什么，然后解释需要添加到存储器中的内容，为什么。之后，你开始重写输入内存，得到更新的内存。
        {new_character_prompt}
        """

    else:
        raise Exception("not supported lang_opt: {}".format(lang_opt))
            
    return input_text