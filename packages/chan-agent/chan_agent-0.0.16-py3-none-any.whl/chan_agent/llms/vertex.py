from functools import cache
from typing import Any
from openai import OpenAI
import instructor
from .base import BaseLLM, register_llm
from chan_agent.llm_track import wrap_create
from typing import Any, Callable

class OpenAICredentialsRefresher(OpenAI):
    def __init__(self, token_fetcher: Callable[[], str], **kwargs: Any) -> None:
        """
        OpenAI 客户端凭据刷新器

        :param token_fetcher: 获取访问令牌的外部方法
        """
        self.token_fetcher = token_fetcher  # 传递的外部方法
        super().__init__(**kwargs, api_key=token_fetcher())

    def _refresh_token(self):
        self.api_key = self.token_fetcher()
        # print(f"update token: {self.api_key[:10]}")

    def __getattribute__(self, name):
        if name == "request":
            self._refresh_token()
        return super().__getattribute__(name)
    


@cache
def init_openai_client(
    project_id: str = "project_id",
    location: str = "asia-east1",
    endpoint_id: str = 'openapi',
    token_fetcher: Callable[[], str] = None  # 额外的参数
):
    """
    初始化 OpenAI 客户端
    """
    if token_fetcher is None:
        raise ValueError("token_fetcher function must be provided")

    # 初始化 OpenAI 客户端，并传递 token_fetcher
    client = OpenAICredentialsRefresher(
        token_fetcher=token_fetcher,
        base_url=f"https://{location}-aiplatform.googleapis.com/v1beta1/projects/{project_id}/locations/{location}/endpoints/{endpoint_id}",
    )

    client.chat.completions.create = wrap_create(create_fn=client.chat.completions.create)
    return client

@register_llm(model_type='vertexai')
class VertexLLM(BaseLLM):
    def __init__(
            self, 
            model_name: str = 'google/gemini-1.5-flash-002',
            base_url: str = None,
            api_key: str = None, 
            **kwargs
        ):
        super().__init__(model_name)
        project_id = kwargs.get('project_id')
        loccation = kwargs.get('location')
        token_fetcher = kwargs.get('token_fetcher')
        endpoint_id = kwargs.get('endpoint_id', 'openapi')
        self.client = init_openai_client(project_id, loccation, endpoint_id, token_fetcher)
     
        self.instructor_client = instructor.from_openai(
            self.client,
            mode=instructor.Mode.JSON
        )
        
    


    


