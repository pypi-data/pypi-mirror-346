from functools import cache
from openai import OpenAI
import instructor
from .base import BaseLLM, register_llm
from chan_agent.llm_track import wrap_create
from chan_agent.logger import logger

@cache
def init_openai_client(base_url:str, api_key:str,**kwargs):
    """
    初始化client客户端
    """
    # 定义openai client
    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
        **kwargs
    )

    client.chat.completions.create = wrap_create(create_fn=client.chat.completions.create)

    return client

@register_llm(model_type="openai")
class OpenaiLLM(BaseLLM):
    def __init__(self, model_name: str = 'gpt-4o-mini', base_url:str=None, api_key:str='xxx'):
        super().__init__(model_name)

        self.client = init_openai_client(base_url = base_url, api_key = api_key)
        if self.model_name is not None and self.model_name.startswith("gpt"):
            instructor_mode = instructor.Mode.TOOLS    
        else:
            # 兼任ollama等openai接口模型的其他模型
            instructor_mode = instructor.Mode.JSON
        self.instructor_client = instructor.from_openai(
            self.client,
            mode=instructor_mode
        )

    def fc_completions_with_messages(
        self, 
        messages: list, 
        functions: list,
        temperature: float = None,
        top_p: float = None,
        max_tokens: int = None,
        timeout: int = 30,
        return_usage: bool = False,
    ):
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                functions=functions,
                stream=False,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                timeout=timeout,
            )
            usage = {
                'completion_tokens': response.usage.completion_tokens,
                'prompt_tokens': response.usage.prompt_tokens,
                'total_tokens': response.usage.total_tokens
            } if response.usage else None
            content = response.choices[0].message.content
            function_call = None
            if response.choices[0].message.function_call:
                function_call = {
                    "name": response.choices[0].message.function_call.name,
                    "arguments": response.choices[0].message.function_call.arguments
                }

            if return_usage:
                return {
                    'content': content,
                    'function_call': function_call,
                    'usage': usage
                }
            else:
                return {
                    'content': content,
                    'function_call': function_call
                }
        except Exception as e:
            logger.error(f"text_completions_with_messages | Error: {e}")
            if return_usage:
                return {
                    'content': "error",
                    'function_call': None,
                    'usage': None
                }
            else:
                return {
                    'content': "error",
                    'function_call': None
                }

    def fc_completions_with_messages_stream(
        self, 
        messages: list, 
        functions: list,
        temperature: float = None,
        top_p: float = None,
        max_tokens: int = None,
        timeout: int = 30,
        return_usage: bool = False,
    ):
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                functions=functions,
                stream=True,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                timeout = timeout,
                stream_options={'include_usage': True}
            )

            full_content = ""
            function_call = None
            function_call_finish = False
            for chunk in response:
                if chunk.choices:
                    choices = chunk.choices[0]
                    if choices.delta.content:
                        full_content += choices.delta.content
                    if choices.delta.function_call:
                        if function_call is None:
                            function_call = {
                                "name": choices.delta.function_call.name,
                                "arguments": choices.delta.function_call.arguments
                            }
                        else:
                            function_call["arguments"] += choices.delta.function_call.arguments
                    if choices.finish_reason == 'function_call':
                        function_call_finish = True

                
                if return_usage:
                    usage = {
                        'completion_tokens': chunk.usage.completion_tokens,
                        'prompt_tokens': chunk.usage.prompt_tokens,
                        'total_tokens': chunk.usage.total_tokens
                    } if chunk.usage else None
                    yield {
                        'content': full_content,
                        'function_call': function_call if function_call_finish else None,
                        'usage': usage
                    }
                else:
                    yield {
                        'content': full_content,
                        'function_call': function_call if function_call_finish else None
                    }                
        except Exception as e:
            logger.error(f"fc_completions_with_messages_stream | Error: {e}")
            if return_usage:
                yield {
                    'content': "error",
                    'function_call': None,
                    'usage': None
                }
            else:
                yield {
                    'content': 'error',
                    'function_call': None
                } 
