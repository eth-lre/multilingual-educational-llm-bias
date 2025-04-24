from typing import Dict, List

from .message import Message


class History(object):
    def __init__(self):
        self.messages = []
        self.turns = 0

    def add_message(self, message: Message):
        self.messages.append(message)
        self.turns += 1

    def __str__(self):
        return "\n\n".join([str(message) for message in self.messages])

    def to_delimited_string(self, delimiter: str):
        return delimiter.join([str(message) for message in self.messages])

    def to_llm_messages(self, role_mapping: Dict[str, str], llm_format: str = "gpt") -> List[Dict[str, str]]:
        if llm_format == "claude":
            return [message.to_claude_format(role_mapping) for message in self.messages]
        elif llm_format == "gpt":
            return [message.to_gpt_format(role_mapping) for message in self.messages]
        elif llm_format == "gemini":
            return [message.to_gemini_format(role_mapping) for message in self.messages]
        elif llm_format == "llama":
            return [message.to_llama_format(role_mapping) for message in self.messages]
        elif llm_format == "mistral":
            return [message.to_mistral_format(role_mapping) for message in self.messages]
        else:
            raise ValueError(f"Unknown LLM format: {llm_format}")
