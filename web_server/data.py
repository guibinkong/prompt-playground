from dataclasses import dataclass
from typing import List


@dataclass
class Options:
    """Class for prompt option."""
    google_model: str = "gemini-pro"
    openai_model: str = "gpt-3.5-turbo"
    cohere_model: str = "command"
    temperature: float = 0.2
    token_limit: int = 128
    top_k: int = 40
    top_p:  float = 0.8


class Example:
    """Class for prompt instance."""
    def __init__(self, input_val, output_val):
        self.input = input_val
        self.output = output_val


@dataclass
class TemplateInstance:
    """Class for prompt template."""
    name: str
    instruction: str
    context: str
    examples: List[Example]


@dataclass
class RetrievalConfig:
    name: str
    urls: List[str]
