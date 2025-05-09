"""
模型适配器
"""
from .client import OpenAIClient
from openai import OpenAI
import os
from volcenginesdkarkruntime import Ark
from llama_index.core.prompts import RichPromptTemplate
from llama_index.llms.openai.utils import to_openai_message_dicts
import requests
from dotenv import load_dotenv
load_dotenv()

class ModelAdapter:
    def __init__(self):
        self.api_key = None
        self.temperature = 0.7
        self.client = None
        self.model_name = None
        self.model_pool = []

    def set_model(self, model_name: str):
        assert model_name in self.model_pool
        self.model_name = model_name
    
    def set_temperature(self, temperature:float):
        self.temperature = temperature

    def get_model(self)->list[str]:
        return self.model_pool

    def product(self, prompt: str) -> str:
        raise NotImplementedError("This method should be implemented by subclasses")

    def chat(self, messages: list) -> str:
        raise NotImplementedError("This method should be implemented by subclasses")


class ModelModalAdapter(ModelAdapter):

    def get_modal_model(self):
        raise NotImplementedError("This method should be implemented by subclasses")
    
    def product_modal(self, prompt: RichPromptTemplate) -> str:
        raise NotImplementedError("This method should be implemented by subclasses")

class BianXieAdapter(ModelModalAdapter):
    """BianXie格式的适配器
    """
    def __init__(self, api_key: str = None, api_base: str = "https://api.bianxie.ai/v1/chat/completions"):
        """初始化

        Args:
            api_key (str): API key for authentication.
            api_base (str): Base URL for the API endpoint.
        """
        super().__init__()
        self.client = OpenAIClient(api_key=api_key or os.getenv('BIANXIE_API_KEY') , api_base=api_base)
        self.model_pool = ['gemini-2.5-flash-preview-04-17-nothinking',
                'gpt-3.5-turbo',
                'gpt-4.1',
                'gpt-4.1-2025-04-14',
                'gpt-4.1-mini',
                'gpt-4.1-mini-2025-04-14',
                'gpt-4.1-nano',
                'gpt-4.1-nano-2025-04-14',
                'gpt-4o',
                'gpt-4o-2024-11-20',
                'gpt-4o-audio-preview',
                'gpt-4o-audio-preview-2024-10-01',
                'gpt-4o-audio-preview-2024-12-17',
                'gpt-4o-all',
                'gpt-4o-image',
                'gpt-4o-image-vip',
                'gpt-4o-mini',
                'gpt-4o-mini-2024-07-18',
                'gpt-4o-mini-audio-preview',
                'gpt-4o-mini-audio-preview-2024-12-17',
                'gpt-4o-mini-realtime-preview',
                'gpt-4o-mini-realtime-preview-2024-12-17',
                'gpt-4o-mini-search-preview',
                'gpt-4o-mini-search-preview-2025-03-11',
                'gpt-4o-realtime-preview',
                'gpt-4o-realtime-preview-2024-10-01',
                'gpt-4o-realtime-preview-2024-12-17',
                'gpt-4o-search-preview-2025-03-11',
                'gpt-4o-search-preview',
                'claude-3-5-haiku-20241022',
                'claude-3-5-haiku-latest',
                'claude-3-5-sonnet-20240620',
                'claude-3-5-sonnet-20241022',
                'claude-3-5-sonnet-20241022-all',
                'claude-3-5-sonnet-all',
                'claude-3-5-sonnet-latest',
                'claude-3-7-sonnet-20250219',
                'claude-3-7-sonnet-20250219-thinking',
                'claude-3-haiku-20240307',
                'coder-claude3.5-sonnet',
                'coder-claude3.7-sonnet',
                'gemini-2.0-flash',
                'gemini-2.0-flash-exp',
                'gemini-2.0-flash-exp-image-generation',
                'gemini-2.0-flash-thinking-exp',
                'gemini-2.0-flash-thinking-exp-01-21',
                'gemini-2.0-pro-exp-02-05',
                'gemini-2.5-flash-preview-04-17',
                'gemini-2.5-flash-preview-04-17-thinking',
                'gemini-2.5-pro-exp-03-25',
                'gemini-2.5-pro-preview-03-25',
                'grok-3',
                'grok-3-beta',
                'grok-3-deepsearch',
                'grok-3-mini-beta',
                'grok-3-fast-beta',
                'grok-3-mini-fast-beta',
                'grok-3-reasoner',
                'grok-beta',
                'grok-vision-beta',
                'o1-mini',
                'o1-mini-2024-09-12',
                'o3-mini',
                'o3-mini-2025-01-31',
                'o3-mini-all',
                'o3-mini-high',
                'o3-mini-low',
                'o3-mini-medium',
                'o4-mini',
                'o4-mini-2025-04-16',
                'o4-mini-high',
                'o4-mini-medium',
                'o4-mini-low',
                'text-embedding-ada-002',
                'text-embedding-3-small',
                'text-embedding-3-large']
        self.model_name = self.model_pool[0]
    
    def get_modal_model(self):
        return ['gpt-4o']
    
    def product_modal(self, prompt: RichPromptTemplate) -> str:
        """Generate a response from the model based on a single prompt.

        Args:
            prompt (str): The input text prompt to generate a response for.

        Returns:
            str: The response generated by the model.
        """
        assert self.model_name in self.get_modal_model()
        messages = to_openai_message_dicts(prompt)
        data = {
            'model': self.model_name,
            'messages': messages,
            'temperature': self.temperature
        }
        return self.client.request(data).get('choices')[0].get('message').get('content')


    def product(self, prompt: str) -> str:
        """Generate a response from the model based on a single prompt.

        Args:
            prompt (str): The input text prompt to generate a response for.

        Returns:
            str: The response generated by the model.
        """
        data = {
            'model': self.model_name,
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': self.temperature
        }
        try:
            return self.client.request(data).get('choices')[0].get('message').get('content')
        except TypeError as e:
            return e
        
    def product_stream(self, prompt: str) -> str:
        """Generate a response from the model based on a single prompt.

        Args:
            prompt (str): The input text prompt to generate a response for.

        Returns:
            str: The response generated by the model.
        """
        data = {
            'model': self.model_name,
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': self.temperature,
            "stream": True
        }
        result_stream = self.client.request_stream(data)
        
        for i in result_stream:
            yield i

    def chat(self, messages: list) -> str:
        """Engage in a conversation with the model using a list of messages.

        Args:
            messages (list): A list of message dictionaries, each containing a role and content.

        Returns:
            str: The response generated by the model for the conversation.
        """
        data = {
            'model': self.model_name,
            'messages': messages,
            'temperature': self.temperature
        }
        try:
            return self.client.request(data).get('choices')[0].get('message').get('content')
        except TypeError as e:
            return e

    def chat_stream(self, messages: list) -> str:
        """Engage in a conversation with the model using a list of messages.

        Args:
            messages (list): A list of message dictionaries, each containing a role and content.

        Returns:
            str: The response generated by the model for the conversation.
        """

        data = {
            "model": self.model_name,
            "messages": messages,
            'temperature': self.temperature,
            "stream": True
        }
        result_stream = self.client.request_stream(data)
        
        for i in result_stream:
            yield i




class KimiAdapter(ModelAdapter):
    """Kimi格式的适配器

    """
    def __init__(self, api_key: str = None, api_base: str = "https://api.moonshot.cn/v1",):
        """初始化

        Args:
            api_key (str): API key for authentication.
            api_base (str): Base URL for the API endpoint.
        """
        super().__init__()
        
        self.client = OpenAI(api_key=api_key or os.getenv('MOONSHOT_API_KEY') , base_url=api_base)
        self.model_pool = ["moonshot-v1-128k","moonshot-v1-128k","moonshot-v1-128k"]
        self.model_name = self.model_pool[0]

    def product(self, prompt: str) -> str:
        """Generate a response from the model based on a single prompt.

        Args:
            prompt (str): The input text prompt to generate a response for.

        Returns:
            str: The response generated by the model.
        """

        data = {
            'model': self.model_name,
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': self.temperature
        }
        return self.client.chat.completions.create(**data).choices[0].message.content

    def chat(self, messages: list) -> str:
        """Engage in a conversation with the model using a list of messages.

        Args:
            messages (list): A list of message dictionaries, each containing a role and content.

        Returns:
            str: The response generated by the model for the conversation.
        """
        data = {
            'model': self.model_name,
            'messages': messages,
            'temperature': self.temperature,
            'stream': True #
        }
        return self.client.chat.completions.create(**data)


class ArkAdapter(ModelAdapter):
    def __init__(self, api_key: str = None, api_base: str = None,):
        """初始化

        Args:
            api_key (str): API key for authentication.
            api_base (str): Base URL for the API endpoint.
        """
        super().__init__()

        self.client = Ark(api_key=api_key or os.getenv('ARK_API_KEY'))
        self.model_pool = ["doubao-1-5-pro-256k-250115"]
        self.model_name = self.model_pool[0]

    def product(self, prompt: str) -> str:
        """Generate a response from the model based on a single prompt.

        Args:
            prompt (str): The input text prompt to generate a response for.

        Returns:
            str: The response generated by the model.
        """
        data = {
            'model': self.model_name,
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': self.temperature
        }
        return self.client.chat.completions.create(**data).choices[0].message.content

    def chat(self, messages: list) -> str:
        """Engage in a conversation with the model using a list of messages.

        Args:
            messages (list): A list of message dictionaries, each containing a role and content.

        Returns:
            str: The response generated by the model for the conversation.
        """
        data = {
            'model': self.model_name,
            'messages': messages,
            'temperature': self.temperature
        }
        return self.client.chat.completions.create(**data).choices[0].message.content


from google.genai import types
from google import genai


class GoogleAdapter(ModelAdapter):
    def __init__(self, api_key: str = None):
        """初始化

        Args:
            api_key (str): API key for authentication.
        """
        super().__init__()
        
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        self.client = genai.Client(api_key=self.api_key)
        self.model_pool = ["gemini-2.5-flash-preview-04-17"]
        self.model_name = self.model_pool[0]
        self.chat_session = None

    def product(self, prompt: str) -> str:
        """Generate a response from the model based on a single prompt.

        Args:
            prompt (str): The input text prompt to generate a response for.

        Returns:
            str: The response generated by the model.
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            config=types.GenerateContentConfig(
                # system_instruction="You are a cat. Your name is Neko.",
                temperature=self.temperature),
            contents=[prompt]
        )
        return response.text

    def chat(self, messages: list) -> str:
        """Engage in a conversation with the model using a list of messages.

        Args:
            messages (list): A list of message dictionaries, each containing a role and content.

        Returns:
            str: The response generated by the model for the conversation.
        """
        # Create a new chat session if one doesn't exist
        if self.chat_session is None:
            self.chat_session = self.client.chats.create(model=self.model_name)
            
        # Get the latest user message (usually the last one in the list)
        latest_message = None
        for msg in reversed(messages):
            if msg.get('role') == 'user':
                latest_message = msg.get('content', '')
                break
                
        if latest_message is None:
            return "No user message found"
            
        # Send the message to the chat session
        response = self.chat_session.send_message(
            latest_message,
            config=types.GenerateContentConfig(
                # system_instruction="You are a cat. Your name is Neko.",
                temperature=self.temperature),
        )
        
        return response.text


def set_llama_index(api_key: str = None, api_base: str = "https://api.bianxieai.com/v1",model:str="gpt-4o",temperature: float =0.1):
    """初始化

    Args:
        api_key (str): API key for authentication.
        api_base (str): Base URL for the API endpoint.
    """

    from llama_index.llms.openai import OpenAI
    from llama_index.core import Settings
    from llama_index.embeddings.openai import OpenAIEmbedding

    api_key=api_key or os.getenv('BIANXIE_API_KEY')

    client = OpenAI(
        model=model,
        api_base=api_base,
        api_key=api_key,
        temperature=temperature,
    )
    Settings.llm = client

    embedding = OpenAIEmbedding(api_base=api_base,api_key=api_key)
    Settings.embed_model = embedding


