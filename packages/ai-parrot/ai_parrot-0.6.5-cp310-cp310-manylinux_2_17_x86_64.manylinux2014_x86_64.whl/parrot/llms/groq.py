from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from navconfig import config
from .abstract import AbstractLLM


class GroqLLM(AbstractLLM):
    """GroqLLM.
        Using Groq Open-source models.
    """
    model: str = "mixtral-8x7b-32768"
    supported_models: list = [
        "llama-3.3-70b-versatile",
        "qwen-2.5-32b",
        "qwen-2.5-coder-32b",
        "deepseek-r1-distill-qwen-32b",
        "deepseek-r1-distill-llama-70b",
        "gemma2-9b-it",
        "llama3-70b-8192",
        "llama3-80b-8192",
        "llama-guard-3-8b",
        "llama-3.1-8b-instant",
        "mistral-saba-24b",
        "mixtral-8x7b-32768",
        "whisper-large-v3",
        "whisper-large-v3-turbo",
    ]

    def __init__(self, *args, **kwargs):
        self.model_type = kwargs.get("model_type", "text")
        system = kwargs.pop('system_prompt', "You are a helpful assistant.")
        human = kwargs.pop('human_prompt', "{question}")
        super().__init__(*args, **kwargs)
        self._api_key = kwargs.pop('api_key', config.get('GROQ_API_KEY'))
        self._llm = ChatGroq(
            model_name=self.model,
            groq_api_key=self._api_key,
            temperature=self.temperature,
            max_retries=self.max_retries,
            max_tokens=self.max_tokens,
            model_kwargs={
                "top_p": self.top_p,
                # "top_k": self.top_k,
            },
        )
        self._embed = None # Not supported
        self.prompt = ChatPromptTemplate.from_messages(
            [("system", system), ("human", human)]
        )
