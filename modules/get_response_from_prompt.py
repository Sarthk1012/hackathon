# import requests
import os

from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

llm = Ollama(
    base_url=os.getenv("LLAMA_AI_URL", ""),
    model="llama2",
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)


def get_response_from_prompt(prompt: str):
    print(llm(prompt))
    # LLAMA_AI_URL = os.getenv("LLAMA_AI_URL", "")
    # url = LLAMA_AI_URL
    # payload = {"model": "llama2", "prompt": prompt}
    # response = requests.post(url, json=payload)
    # headers = {"Authorization": "Bearer PMV23XXGX62XNNAYQPEMBM7B4DMVR6ZT"}
    # response = requests.get(url, headers=headers)
    # if response.status_code == 200:
    #     generated_text = response.json().get("text", "")
    #     print("generated_text", generated_text)
    #     return generated_text
    # else:
    #     print(f"Request failed with status code: {response.status_code}")
    #     return None
