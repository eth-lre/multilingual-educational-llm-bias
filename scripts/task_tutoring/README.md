## About
Multilingual MathDial extends the MathDial dataset and framework ([ArXiv paper](https://arxiv.org/abs/2305.14536), [EMNLP 2023 Video](https://s3.amazonaws.com/pf-user-files-01/u-59356/uploads/2023-11-13/6a13y89/mathdial-emnlp23-v5.mp4), [GitHub repository](https://github.com/eth-nlped/mathdial/)) to support multiple languages and offers plug-and-play compatibility with various Large Language Models (LLMs). This makes it easier to evaluate dialogue tutoring models for their multi-linguistic properties.

## Setup
Create a file `load_key.py` in `model` to store all your API keys with identifiers (or edit the calling commands accordingly):
- Azure_KEY_VAN
- GPT_KEY_VAN
- Google_KEY_VAN
- Mistral_KEY_VAN
- Fireworks_KEY_VAN (For Llama)
- Anthropic_KEY
- Cohere_KEY

## Teacher model - Generate next tutor response

Note: You can tune other experiment parameters like model_name and max_utterances in `params.py`

```bash
python -m src.llm_baseline
```
Please see `src/teachers.py` and `src/llm.py` to add your own teacher model. A corresponding change is required in `src/message.py` and `src/history.py` as well.

## Evaluate your teacher model using simulated student
```bash
python -m src.evaluate 
```
