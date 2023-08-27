# import requests
import os

from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


def get_response_from_prompt(prompt: str):
    llm = Ollama(
        base_url=os.getenv("LLAMA_AI_URL", ""),
        model="llama2",
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )
    return llm(prompt)
