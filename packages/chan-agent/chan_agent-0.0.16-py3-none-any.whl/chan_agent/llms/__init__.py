from .base import BaseLLM, LLM_REGISTRY
from .async_base import AsyncBaseLLM
from .openai import OpenaiLLM
from .gemini import GeminiLLM
from .vertex import VertexLLM
from .async_openai import AsyncOpenaiLLM
from .async_vertex import AsyncVertexLLM
from functools import cache


@cache
def get_llm(llm_type:str, model_name:str,  base_url:str, api_key:str, **kwargs) -> BaseLLM:
    """
    获取llm
    """
    if llm_type not in LLM_REGISTRY:
        raise ValueError(f"Invalid llm_type: {llm_type}. Must be one of {list(LLM_REGISTRY.keys())}.")
   
    return LLM_REGISTRY[llm_type](model_name, base_url, api_key, **kwargs)


__all__ = [
    'BaseLLM',
    'AsyncBaseLLM',
    'LLM_REGISTRY',
    'get_llm',
]