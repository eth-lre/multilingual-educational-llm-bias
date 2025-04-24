import openai
import google.generativeai as genai
from mistralai import Mistral, SystemMessage
from cohere import ClientV2
import anthropic
import json
from .load_key import *
import time
from ..params import *


class PlaceholderContent:
    def __init__(self, text):
        self.parts = [self.Part(text)]

    class Part:
        def __init__(self, text):
            self.text = text


class PlaceholderResponse:
    def __init__(self, text="No response from Gemini"):
        self.candidates = [self.Candidate(text)]

    class Candidate:
        def __init__(self, text):
            self.content = PlaceholderContent(text)


class LLM:
    def __init__(self, key, model):
        self.key = key
        self.model_name = model

    def get_completion(self, messages, system_prompt, TEMP, outputs=1):
        raise NotImplementedError(
            "This method should be overridden by subclasses")

    def attempt_completion(self, messages, system_prompt, stop, TEMP, outputs=1):
        for attempt in range(1, max_attempts + 1):
            try:
                return self.get_completion(messages, system_prompt, stop, TEMP, outputs)
            except Exception as e:
                print(
                    "X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X")
                print(
                    "X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X")
                print(f"Attempt {attempt} failed. Error: {e}")
                if attempt < max_attempts:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"Max attempts reached. Exiting.")
                    raise


class Cohere(LLM):
    def __init__(self, key, model="claude-3-5-sonnet-20240620"):
        super().__init__(key, model)

    def get_completion(self, messages, system_prompt, stop, TEMP, outputs=1, logprobs=False, top_logprobs=None):

        client = ClientV2(self.key)
        messages = [{"role": "system", "content": system_prompt}, *messages]
        responses = []
        for i in range(outputs):
            responses.append(client.chat(
                model=self.model_name,
                messages=messages,
                # n=1,
                # response_format={"type": "json_object"},
                temperature=TEMP,
                max_tokens=512, #Required by Claude
                # seed = seed_val,
                # stop_sequences = stop,
                # logprobs=logprobs,
                # top_logprobs=top_logprobs,
            ))

        return responses


class Claude(LLM):
    def __init__(self, key, model="claude-3-5-sonnet-20240620"):
        super().__init__(key, model)

    def get_completion(self, messages, system_prompt, stop, TEMP, outputs=1, logprobs=False, top_logprobs=None):

        client = anthropic.Anthropic(api_key=self.key)

        responses = []
        for i in range(outputs):
            responses.append(client.messages.create(
                model=self.model_name,
                system = system_prompt,
                messages=messages,
                # n=1,
                # response_format={"type": "json_object"},
                temperature=TEMP,
                max_tokens=512, #Required by Claude
                # seed = seed_val,
                # stop_sequences = stop,
                # logprobs=logprobs,
                # top_logprobs=top_logprobs,
            ))

        return responses


class Gemini(LLM):
    def __init__(self, key, model="gemini-1.5-pro"):
        super().__init__(key, model)

    def get_completion(self, messages, system_prompt, stop, TEMP, outputs=1):
        genai.configure(api_key=self.key)
        GeminiModel = genai.GenerativeModel(self.model_name, system_instruction=system_prompt, generation_config={
                                            "candidate_count": 1,
                                            # "max_output_tokens": 512,
                                            "temperature": TEMP})
        responses = []
        for i in range(outputs):
            temp_gemini_response = GeminiModel.generate_content(messages)
            # print(temp_gemini_response)
            if temp_gemini_response and hasattr(temp_gemini_response, 'candidates') and temp_gemini_response.candidates:
                responses.append(temp_gemini_response)
            else:
                responses.append(PlaceholderResponse())

        return [response.candidates[0] for response in responses]


class GPT(LLM):
    def __init__(self, key, model="gpt-4o"):
        super().__init__(key, model)

    def get_completion(self, messages, system_prompt, stop, TEMP, outputs=1, logprobs=False, top_logprobs=None):

        openai.api_key = self.key

        messages = [{"role": "system", "content": system_prompt}, *messages]
        response = openai.chat.completions.create(
            model=self.model_name,
            messages=messages,
            n=outputs,
            # response_format={"type": "json_object"},
            temperature=TEMP,
            # max_tokens=512,
            # seed = seed_val,
            # stop=stop,
            logprobs=logprobs,
            top_logprobs=top_logprobs,
        )
        return response.choices


class Llama(LLM):
    def __init__(self, key, model="llama-13b-chat"):
        super().__init__(key, model)

    def get_completion(self, messages, system_prompt, stop, TEMP, outputs=1, logprobs=False, top_logprobs=None):

        client = openai.OpenAI(
            api_key=self.key,
            base_url="https://api.fireworks.ai/inference/v1"
        )

        messages = [
            {"role": "system",
             "content": system_prompt
             }, *messages]

        responses = []
        for i in range(outputs):
            responses.append(client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                n=1,
                # response_format={"type": "json_object"},
                temperature=TEMP,
                # max_tokens=512,
                # seed = seed_val,
                logprobs=logprobs,
                top_logprobs=top_logprobs,
            ).choices)

        return responses


class MistralClass(LLM):
    def __init__(self, key, model="..."):
        super().__init__(key, model)

    def get_completion(self, messages, system_prompt, stop, TEMP, outputs=1):
        messages = [SystemMessage(content=system_prompt), *messages]
        client = Mistral(api_key=self.key)
        responses = []
        for i in range(outputs):
            responses.append(client.chat.complete(model=self.model_name,
                             messages=messages,
                             temperature=TEMP,
                                                  #  max_tokens=512,
                            #  stop=stop
                             ).choices)
        return responses
