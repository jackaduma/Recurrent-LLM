# Recurrent-LLM
The Open Source LLM implementation of paper: RecurrentGPT: Interactive Generation of (Arbitrarily) Long Text

## Global Config
[global_config.py](./global_config.py)

```
lang_opt = "zh" #  zh or en. make English or Chinese Novel
llm_model_opt = "openai" # default is openai, it also can be "vicuna" or "chatglm" or "baichuan" etc.
```

## OpenAI - ChatGPT

you should apply an openai api key first. then
```
export OPENAI_API_KEY = "your key"
```

## Vicuna 

download vicuna model. and config it in [models/vicuna_bin.py](models/vicuna_bin.py)

## ChatGLM

```python
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path,trust_remote_code=True)
model_config = AutoConfig.from_pretrained(model_name_or_path, trust_remote_code=True)
model = AutoModel.from_pretrained(model_name_or_path, config=model_config, trust_remote_code=True)
```

## Baichuan

```python
tokenizer = AutoTokenizer.from_pretrained("baichuan-inc/baichuan-7B", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("baichuan-inc/baichuan-7B", device_map="auto", trust_remote_code=True)
```

## WebUI

<img src="./imgs/webui-snapshot.png">