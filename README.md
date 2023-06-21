## **Recurrent-LLM**
The Open Source LLM implementation of paper: 

**RecurrentGPT: Interactive Generation of (Arbitrarily) Long Text**.

[[Paper](https://arxiv.org/pdf/2305.13304v1.pdf)] [[arxiv](https://arxiv.org/abs/2305.13304v1)] [[HuggingFace](https://huggingface.co/papers/2305.13304)] [[Offical](https://github.com/aiwaves-cn/RecurrentGPT)]

The fixed-size context of Transformer makes GPT models incapable of generating arbitrarily long text. In this paper, we introduce RecurrentGPT, a language-based simulacrum of the recurrence mechanism in RNNs. RecurrentGPT is built upon a large language model (LLM) such as ChatGPT and uses natural language to simulate the Long Short-Term Memory mechanism in an LSTM. At each timestep, RecurrentGPT generates a paragraph of text and updates its language-based long-short term memory stored on the hard drive and the prompt, respectively. This recurrence mechanism enables RecurrentGPT to generate texts of arbitrary length without forgetting. Since human users can easily observe and edit the natural language memories, RecurrentGPT is interpretable and enables interactive generation of long text. RecurrentGPT is an initial step towards next-generation computer-assisted writing systems beyond local editing suggestions. In addition to producing AI-generated content (AIGC), we also demonstrate the possibility of using RecurrentGPT as an interactive fiction that directly interacts with consumers. We call this usage of generative models by ``AI As Contents'' (AIAC), which we believe is the next form of conventional AIGC. We further demonstrate the possibility of using RecurrentGPT to create personalized interactive fiction that directly interacts with readers instead of interacting with writers. More broadly, RecurrentGPT demonstrates the utility of borrowing ideas from popular model designs in cognitive science and deep learning for prompting LLMs. 

Transformer的固定尺寸上下文使得GPT模型无法生成任意长的文本。在本文中，我们介绍了RecurrentGPT，一个基于语言的模拟RNNs中的递归机制。RecurrentGPT建立在大型语言模型（LLM）之上，如ChatGPT，并使用自然语言来模拟LSTM中的长短时记忆机制。在每个时间段，RecurrentGPT生成一段文字，并更新其基于语言的长短时记忆，分别存储在硬盘和提示器上。这种递归机制使RecurrentGPT能够生成任意长度的文本而不被遗忘。由于人类用户可以很容易地观察和编辑自然语言记忆，因此RecurrentGPT是可解释的，并能互动地生成长文本。RecurrentGPT是朝着超越本地编辑建议的下一代计算机辅助写作系统迈出的第一步。除了制作人工智能生成的内容（AIGC），我们还展示了使用RecurrentGPT作为直接与消费者互动的互动小说的可能性。我们称这种生成模型的使用为 "AI As Contents"（AIAC），我们认为这是传统AIGC的下一个形式。我们进一步展示了使用RecurrentGPT创造个性化互动小说的可能性，这种小说直接与读者互动，而不是与作者互动。更广泛地说，RecurrentGPT证明了从认知科学和深度学习中流行的模型设计中借用思想来提示LLM的效用。

---

## **Table of Contents**
- [**Recurrent-LLM**](#recurrent-llm)
- [**Table of Contents**](#table-of-contents)
- [**Requirements**](#requirements)
- [**Configuration**](#configuration)
  - [**Global Config**](#global-config)
  - [**Supported LLM options**](#supported-llm-options)
    - [**OpenAI ChatGPT**](#openai-chatgpt)
    - [**Vicuna**](#vicuna)
    - [**ChatGLM**](#chatglm)
    - [**Baichuan**](#baichuan)
    - [**Aquila**](#aquila)
    - [**Falcon**](#falcon)
- [**Usage**](#usage)
  - [**start web server**](#start-web-server)
- [**WebUI**](#webui)
- [**Star-History**](#star-history)
- [**License**](#license)

## **Requirements**

```
pip install transformers@git+https://github.com/huggingface/transformers.git
pip install peft@git+https://github.com/huggingface/peft.git
pip install accelerate@git+https://github.com/huggingface/accelerate.git
pip install bitsandbytes==0.39.0

pip install -U flagai
pip install bminf
```

## **Configuration** 

### **Global Config**
[[global_config.py](./global_config.py)]

```
lang_opt = "zh" #  zh or en. make English or Chinese Novel
llm_model_opt = "openai" # default is openai, it also can be other open-source LLMs as below
```

### **Supported LLM options**

- [x] openai
- [x] vicuna
- [x] chatglm
- [x] baichuan
- [x] aquila
- [x] falcon 

#### **OpenAI ChatGPT**

you should apply an openai api key first. then
```
export OPENAI_API_KEY = "your key"
```

#### **Vicuna**

download vicuna model. and config it in [models/vicuna_bin.py](models/vicuna_bin.py)

#### **ChatGLM**

```python
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path,trust_remote_code=True)
model_config = AutoConfig.from_pretrained(model_name_or_path, trust_remote_code=True)
model = AutoModel.from_pretrained(model_name_or_path, config=model_config, trust_remote_code=True)
```

#### **Baichuan**

```python
tokenizer = AutoTokenizer.from_pretrained("baichuan-inc/baichuan-7B", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("baichuan-inc/baichuan-7B", device_map="auto", trust_remote_code=True)
```

#### **Aquila**

```python
loader = AutoLoader(
        "lm",
        model_dir=state_dict,
        model_name=model_name,
        use_cache=True,
        fp16=True)
model = loader.get_model()
tokenizer = loader.get_tokenizer()
model.eval()
```
If want to use bminf, then add code as below:
```python
with torch.cuda.device(0):
    model = bminf.wrapper(model, quantization=False, memory_limit=2 << 30)
```


#### **Falcon**


## **Usage**

### **start web server**

```
python gradio_server.py
```


## **WebUI**

<img src="./imgs/webui-snapshot.png">

------
## **Star-History**

![star-history](https://api.star-history.com/svg?repos=jackaduma/Recurrent-LLM&type=Date "star-history")

------

## **License**

[MIT](LICENSE) © Kun