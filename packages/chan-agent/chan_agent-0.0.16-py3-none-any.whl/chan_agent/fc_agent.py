import json
from .logger import logger
from textwrap import dedent
from .llms import BaseLLM
from .base_tool import BaseTool
from .schema import *
from .utils.messages_processing import get_messages_conversation_format_openai
from typing import List, Union, Optional, Iterator, Literal


PROMPT_ROLE_SECTION = dedent("""\
# Role
{role}

""")


PROMPT_RULES_SECTION = dedent("""\
# Rules
- Maintain a polite and professional tone at all times
{rules}

{extra_info}

""")


class FCAgent:

    def __init__(
        self, 
        llm: BaseLLM,
        role: str, 
        tools: List[BaseTool],
        rules: List[str],
        static_extra_info: Optional[str] = "",
        agent_type: Literal["user", "assistant"] = "assistant",
        max_content_chat_length: int = 6,
        max_llm_call_per_run: int = 3,
    ):

        self.role = role
        self.tools_map = {tool.name: tool for tool in tools}
        self.tools_desc = "\n".join([str(tool) for tool in tools])
        self.rules_desc = "\n".join([f"- {rule}" for rule in rules])
        self.static_extra_info = static_extra_info

        # 最大每一轮工具使用的轮数
        self.max_llm_call_per_run = max_llm_call_per_run
        # 最大对话上下文的轮数
        self.max_content_chat_length = max_content_chat_length
        # agent类型
        self.agent_type = agent_type

        self.llm = llm
        self.usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

    def record_usage(self, usage: dict):
        """
        缓存usage
        """
        if usage:
            self.usage["total_tokens"] += usage.get("total_tokens", 0)
            self.usage["prompt_tokens"] += usage.get("prompt_tokens", 0)
            self.usage["completion_tokens"] += usage.get("completion_tokens", 0)
    
    def clear_usage(self):
        """
        清除usage
        """
        self.usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

    def get_usage(self):
        """
        获取usage
        """
        return self.usage


    def make_agent_messages(self, messages:List[AgentMessage], **kwargs) -> str:
        """
        构建agent messages
        """

        # 仅保留max_content_chat_length长度的上下文
        conversations = get_messages_conversation_format_openai(messages, max_content_chat_length=self.max_content_chat_length)

        system_prompt = ""
        system_prompt += PROMPT_ROLE_SECTION.format(role=self.role)
        system_prompt += PROMPT_RULES_SECTION.format(
            rules=self.rules_desc, 
            extra_info=self.static_extra_info + kwargs.get("dynamic_extra_info", "")
        )

        return [{'role': 'system', 'content': system_prompt}] + conversations
    
    def __detect_tool(self, content:dict) -> Union[ToolCall, SystemError, None]:
        """
        检测工具
        """
        try:
            tool_call = ToolCall(name = content['function_call'].get("name"), args = json.loads(content['function_call'].get("arguments", {}))) if content.get('function_call') else None
            return tool_call
        except Exception as e:
            return SystemError(error=str(e))

    def chat(self, messages:List[AgentMessage], do_tool_call:bool=True, **kwargs) -> List[AgentMessage]:
        """
        对话
        """
        # 清除usage
        self.clear_usage()

        num_llm_calls_available = self.max_llm_call_per_run
        response = []
        while True and num_llm_calls_available > 0:
            system_error = None

            num_llm_calls_available -= 1

            # 生成agent prompt
            agent_messages = self.make_agent_messages(messages=messages+response, **kwargs)

            # 发起llm请求
            out_dict = self.llm.fc_completions_with_messages(
                messages=agent_messages,
                functions = [tool.to_function() for tool in self.tools_map.values()],
                temperature=kwargs.get('temperature', 0.3),
                top_p=kwargs.get('top_p', None),
                max_tokens=kwargs.get('max_tokens', None),
                return_usage=True
            )

            # 记录usage
            self.record_usage(out_dict.get('usage', {}))

            # 检测使用的工具
            tool_call = self.__detect_tool(out_dict)

            response.append(AgentMessage(
                role=self.agent_type,
                content=out_dict['content'] or '',
                tool_call=None if isinstance(tool_call, SystemError) else tool_call,
            ))
            if isinstance(tool_call, SystemError):
                system_error = tool_call
                

            if do_tool_call and isinstance(tool_call, ToolCall):
                # 执行工具
                logger.info(tool_call)
                tool_result = self.tools_map[tool_call.name].call(params=tool_call.args, **kwargs)
                response.append(AgentMessage(
                    role=tool_call.name,
                    content=tool_result.response,
                    extra=tool_result.extra,
                ))
                if tool_result.use_tool_response:
                    response.append(AgentMessage(
                        role=self.agent_type,
                        content=tool_result.response,
                    ))
            elif system_error:
                response.append(AgentMessage(
                    role="system",
                    content=tool_call.error,
                ))
            else:
                break 
                
        return response


    def chat_with_stream(self, messages:List[AgentMessage], do_tool_call:bool=True, **kwargs) -> Iterator[List[AgentMessage]]:
        """
        流式对话
        """
        # 清除usage
        self.clear_usage()
        num_llm_calls_available = self.max_llm_call_per_run
        response = []
        while True and num_llm_calls_available > 0:
            system_error = None
            
            num_llm_calls_available -= 1

            # 生成agent prompt
            agent_messages = self.make_agent_messages(messages=messages+response, **kwargs)

            # 发起llm请求
            llm_out = self.llm.fc_completions_with_messages_stream(
                messages=agent_messages, 
                functions=[tool.to_function() for tool in self.tools_map.values()],
                temperature=kwargs.get('temperature', 0.3),
                top_p=kwargs.get('top_p', None),
                max_tokens=kwargs.get('max_tokens', None),
                return_usage=True
            )

            agent_output = AgentMessage(role=self.agent_type, content='')
            for out_dict in llm_out:
                # 检测使用的工具
                tool_call = self.__detect_tool(out_dict)
                agent_output.content = out_dict['content'] or ''
                agent_output.tool_call = None if isinstance(tool_call, SystemError) else tool_call
                self.record_usage(out_dict.get('usage', {}))

                yield response + [agent_output]

                if tool_call is not None:
                    # 已经识别到工具直接截断
                    if isinstance(tool_call, SystemError):
                        system_error = tool_call
                    # break
            
            response += [agent_output]
            
            if do_tool_call and isinstance(agent_output.tool_call, ToolCall):
                # 执行工具
                logger.info(agent_output.tool_call)

                tool_result = self.tools_map[tool_call.name].call(params=tool_call.args, **kwargs)
                response.append(AgentMessage(
                    role=tool_call.name,
                    content=tool_result.response,
                    extra=tool_result.extra,
                ))
                yield response
                if tool_result.use_tool_response:
                    # 使用工具的回复
                    response.append(AgentMessage(
                        role=self.agent_type,
                        content=tool_result.response,
                    ))
                    yield response
                    break
            elif system_error:
                response.append(AgentMessage(
                    role="system",
                    content=system_error.error,
                ))
                yield response
            else:
                break 
                        
        