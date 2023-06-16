# Recurrent-LLM
The Open Source LLM implementation of paper: RecurrentGPT: Interactive Generation of (Arbitrarily) Long Text

## Global Config
[global_config.py](./global_config.py)

```
lang_opt = "zh" #  zh or en. make English or Chinese Novel
llm_model_opt = "openai" # default is openai, it also can be "vicuna" or "chatglm"
```

## OpenAI - ChatGPT

you should apply an openai api key first. then
```
export OPENAI_API_KEY = "your key"
```

## Vicuna 

download vicuna model. and config it in [models/vicuna_bin.py](models/vicuna_bin.py)

## ChatGLM