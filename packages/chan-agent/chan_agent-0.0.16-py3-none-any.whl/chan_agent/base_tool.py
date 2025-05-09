import json
from abc import ABC, abstractmethod
from typing import List, Optional, Union
from .logger import logger
from .schema import ToolResult

TOOL_REGISTRY = {}


def register_tool(name, allow_overwrite=False):

    def decorator(cls):
        if name in TOOL_REGISTRY:
            if allow_overwrite:
                logger.warning(f'Tool `{name}` already exists! Overwriting with class {cls}.')
            else:
                raise ValueError(f'Tool `{name}` already exists! Please ensure that the tool name is unique.')
        if cls.name and (cls.name != name):
            raise ValueError(f'{cls.__name__}.name="{cls.name}" conflicts with @register_tool(name="{name}").')
        cls.name = name
        TOOL_REGISTRY[name] = cls

        return cls

    return decorator


def schema_to_str(schema: Union[List[dict], dict], indent_level=0):
    """
    转换为字符串描述
    """
    output = []
    
    # 设置缩进
    indent = "  " * indent_level

    for key in schema:
        type_ = schema[key].get('type')
        description = schema[key].get('description', '')
        items = schema[key].get('items', {})
        properties = schema[key].get('properties', {})
        required = schema[key].get('required', True)

        if type_ == 'array' and items:
            # 数组
            item_type = items.get('type')
            item_properties = items.get('properties', {})
            if item_type == 'object' and item_properties:
                output.append(f"{indent}- `{key}`: list[object] {description}, each object with the following properties:")
                output.extend(schema_to_str(item_properties, indent_level + 1))
            else:
                output.append(f"{indent}- `{key}`: list[{item_type}], {description}")

        elif type_ == 'object' and properties:
            # 如果是对象
            output.append(f"{indent}- `{key}`: object {description}, with the following properties:")
            output.extend(schema_to_str(properties, indent_level + 1))
        else:
            output.append(f"{indent}- `{key}`: {type_ if required else f'Optional[{type_}]'} {description}")
        
    return output

    

class BaseTool(ABC):
    name: str = ''
    description: str = ''
    parameters: List[dict] = {
        'your_key_name': {
            'type': 'array',
            'items': {
                'type': 'number',
            },
            'description': 'your key description',
            'required': True
        },
    }

    def __init__(self, cfg: Optional[dict] = None):
        self.cfg = cfg or {}
        if not self.name:
            raise ValueError(
                f'You must set {self.__class__.__name__}.name, either by @register_tool(name=...) or explicitly setting {self.__class__.__name__}.name'
            )

    def __str__(self):
        output = []
        
        # 名称和描述
        output.append(f"- {self.name}: {self.description}, with the following input parameters:")

        output.extend(schema_to_str(self.parameters, 1))

        return '\n'.join(output)
    
    def to_function(self) -> dict:
        """
        Convert the tool to a function format compatible with OpenAI Function Calling.
        """
        def process_schema(schema):
            """
            递归处理 JSON Schema，提取 required 字段，并转换格式。
            """
            if not isinstance(schema, dict):
                return schema
            
            properties = {}
            required_fields = []
            
            for key, value in schema.items():
                if isinstance(value, dict):
                    new_value = value.copy()
                    
                    if "items" in value and value['items']['type'] == 'object':
                        new_value['items'] = process_schema(value['items']['properties'])

                    # 递归处理嵌套结构（如 properties）
                    if "properties" in value:
                        new_value["properties"] = process_schema(value["properties"])

                    # 提取 required 信息并更新属性
                    if "required" in value and value["required"]:
                        required_fields.append(key)
                    
                    # 删除嵌套结构中的 required 字段
                    new_value.pop("required", None)

                    properties[key] = new_value
            
            # 构建最终的 schema
            output_schema = {"type": "object", "properties": properties}
            if required_fields:
                output_schema["required"] = required_fields

            return output_schema

        # 处理并格式化参数 schema
        processed_parameters = process_schema(self.parameters)
        
        return {
            "name": self.name,
            "description": self.description or "No description available.",
            "parameters": processed_parameters
        }
        
        

    def call(self, params: Union[str, dict], **kwargs) -> ToolResult:
        """The interface for calling tools.

        Each tool needs to implement this function, which is the workflow of the tool.

        Args:
            params: The parameters of func_call.
            kwargs: Additional parameters for calling tools.

        Returns:
            The result returned by the tool, implemented in the subclass.
        """
        pass

    async def async_call(self, params: Union[str, dict], **kwargs) -> ToolResult:
        """The async interface for calling tools.

        By default, this method wraps the synchronous call method. Override this method
        if you need to implement asynchronous operations.

        Args:
            params: The parameters of func_call.
            kwargs: Additional parameters for calling tools.

        Returns:
            The result returned by the tool.
        """
        pass
        

    def _verify_json_format_args(self, params: Union[str, dict]) -> dict:
        """Verify the parameters of the function call"""
        if isinstance(params, str):
            try:
                params_json: dict = json.loads(params)
            except json.decoder.JSONDecodeError:
                raise ValueError('Parameters must be formatted as a valid JSON!')
        else:
            params_json: dict = params
        
        # TODO 验证参数格式

        return params_json

