"""
MarkPrompt client implementation.
"""
import inspect
import os
from pathlib import Path
from typing import Dict, Optional, Union, List, Callable, Any, TypeVar

from openai import OpenAI

# 定义类型变量
ResponseFormatT = TypeVar("ResponseFormatT")

from .core import TemplateParser
from .core.logger import setup_logger, message_logger, DynamicLogger, format_tool_calls
from .core.tools import ToolHandler

logger = setup_logger(__name__)


class MarkPromptClient:
    """Client for generating responses using MarkPrompt templates."""

    # 存储已注册的自定义 provider
    _registered_providers = {}

    def __init__(self, template_dir: Union[str, Path] = '.', client: Optional[OpenAI] = None):
        """Initialize the client.
        
        Args:
            template_dir: Directory containing prompt templates. Can be a string or Path object.
            client: Optional OpenAI client instance. If not provided, a default OpenAI client will be used.
        """
        if isinstance(template_dir, str):
            # 处理 ~ 开头的路径
            if template_dir.startswith("~"):
                template_dir = os.path.expanduser(template_dir)

            # 如果是相对路径，从调用者的文件位置开始查找
            if not os.path.isabs(template_dir):
                caller_frame = inspect.stack()[1]
                caller_file = caller_frame.filename
                caller_dir = os.path.dirname(os.path.abspath(caller_file))
                template_dir = os.path.join(caller_dir, template_dir)

            template_dir = Path(template_dir)

        if not template_dir.is_dir():
            raise ValueError(f"Template directory not found: {template_dir}")

        self.template_dir = template_dir
        print(f"template_dir: {self.template_dir}")
        self.client = client if client else OpenAI()
        self.parser = TemplateParser()
        

    @classmethod
    def register_provider(cls, name: str, provider_factory: Callable[[Dict[str, Any]], Any]) -> None:
        """注册自定义 provider 工厂函数。
        
        Args:
            name: provider 的唯一名称
            provider_factory: 根据配置创建 provider 实例的工厂函数
                该函数接收配置字典作为参数，返回兼容 OpenAI 接口的客户端实例
        
        Example:
            ```python
            # 自定义 provider 工厂函数
            def my_provider_factory(config):
                # 这里可以对配置进行处理，然后返回 OpenAI 兼容的客户端实例
                return CustomClient(**config)
                
            # 注册自定义 provider
            MarkPromptClient.register_provider("litellm", my_provider_factory)
            ```
        """
        cls._registered_providers[name] = provider_factory

    def _create_client_from_provider(self, provider_config: Dict[str, Any]) -> OpenAI:
        """根据提供商配置创建 OpenAI 客户端。
        
        Args:
            provider_config: 提供商配置字典，可以包含 'name' 字段指定使用的 provider
            
        Returns:
            初始化好的 OpenAI 客户端或兼容的客户端
        """
        # 检查配置中是否指定了已注册的自定义 provider
        provider_name = provider_config.get("name")
        if provider_name and provider_name in self._registered_providers:
            # 移除 name 字段，避免传递给工厂函数
            config_copy = provider_config.copy()
            config_copy.pop("name")
            # 使用注册的工厂函数创建客户端
            return self._registered_providers[provider_name](config_copy)

        # 使用默认的 OpenAI 客户端创建逻辑
        openai_params = [
            "api_key", "base_url", "timeout", "max_retries",
            "default_headers", "default_query", "organization",
            "project_id", "api_version"
        ]

        client_kwargs = {}
        for key, value in provider_config.items():
            if key in openai_params:
                client_kwargs[key] = value

        return OpenAI(**client_kwargs)

    def _generate_with_tools(self, messages, tools: List[Callable], verbose: bool = False, client=None, **params):
        tool_handler = ToolHandler(tools=tools, verbose=verbose)
        openai_tools = tool_handler.convert_tools_to_openai_format()
        client_to_use = client if client is not None else self.client

        with DynamicLogger() as alogger:

            response = client_to_use.chat.completions.create(
                messages=messages,
                tools=openai_tools,
                **params
            )

            if response.choices[0].message.tool_calls is None:
                panel_content = response.choices[0].message.content
                alogger.log(panel_content)
                return response

            if verbose:
                content = format_tool_calls(response.choices[0].message.tool_calls)
                alogger.log(content)

            tool_results = tool_handler.execute_tool_calls(
                response.choices[0].message.tool_calls
            )

            if tool_results:
                try:
                    new_messages = messages.copy()
                    new_messages.append({
                        "role": "assistant",
                        "tool_calls": response.choices[0].message.tool_calls
                    })
                    new_messages.extend(tool_results)
                    second_response = client_to_use.chat.completions.create(
                        messages=new_messages,
                        **params
                    )

                    if verbose:
                        alogger.log("\n\n")
                        panel_content = second_response.choices[0].message.content
                        alogger.log(panel_content)
                    return second_response
                except Exception as e:
                    if verbose:
                        print(f"{str(e)}")
                        logger.error(f"二次请求失败: {str(e)}")
                        panel_content += f"\n\n生成失败: {str(e)}"
                        logger.error(f"二次请求失败: {panel_content}")
                    return response

    def _generate_common(
            self,
            template_name: str,
            user_message: Union[str, Dict[str, Any], List[Dict[str, Any]]],
            input_variables: Optional[Dict[str, str]] = None,
            verbose: bool = False,
            tools: Optional[List[Callable]] = None,
            use_beta_api: bool = False,
            **override_params
    ):
        """Common implementation for generate and generate_beta."""
        template_path = self.template_dir / f"{template_name}.md"
        if not template_path.exists():
            raise ValueError(f"Template not found: {template_name}")

        with open(template_path, "r", encoding="utf-8") as f:
            # 传递模板文件的完整路径作为参数，用于处理相对路径
            template = self.parser.parse(f.read(), str(template_path))

        # 默认使用已初始化的客户端
        client = self.client

        # 如果模板中定义了 provider 配置，创建临时客户端实例
        if template.provider:
            try:
                temp_client = self._create_client_from_provider(template.provider)
                client = temp_client
                if verbose:
                    logger.info(f"Using template-specific provider: {template.provider.get('name', 'unknown')}")
            except Exception as e:
                logger.error(f"创建模板特定客户端失败: {str(e)}，使用默认客户端")

        messages = self.parser.render(template, input_variables)
        if messages[-1]['role'] != 'user':
            if isinstance(user_message, dict):
                user_msg = user_message
            else:
                user_msg = {"role": "user", "content": user_message}

            if verbose:
                print(f"User message: {user_msg}")
            messages.append(user_msg)

        # 无论是在终端还是Jupyter Notebook中，都根据verbose控制日志输出
        message_logger.log_messages(messages, verbose=verbose)

        params = {k: v for k, v in template.generation_config.items() if v is not None}
        params.update(override_params)

        if tools:
            # Tool handling is the same for both APIs
            response = self._generate_with_tools(messages, tools, verbose, client=client, **params)
        else:
            if use_beta_api:
                # Use beta API
                response = client.beta.chat.completions.parse(
                    messages=messages,
                    **params
                )
            else:
                # Use standard API
                response = client.chat.completions.create(
                    messages=messages,
                    **params
                )

            # 无论是在终端还是Jupyter Notebook中，都根据verbose控制日志输出
            if hasattr(response, 'choices') and hasattr(response.choices[0], 'message'):
                message = response.choices[0].message
                message_logger.log_message(message.__dict__, verbose=verbose)

        return response

    def generate(
            self,
            template_name: str,
            user_message: Union[str, Dict[str, Any], List[Dict[str, Any]]],
            input_variables: Optional[Dict[str, str]] = None,
            verbose: bool = False,
            tools: Optional[List[Callable]] = None,
            **override_params
    ):
        """Generate a response using the specified template.
        
        Args:
            template_name: Name of the template file (without .md extension)
            user_message: User message content. Can be str, dict, or list.
            input_variables: Optional template variables
            verbose: Optional flag to enable verbose logging
            tools: Optional list of functions to be converted to OpenAI tools/function calling
            **override_params: Parameters to override template's generate_config,
                             including 'stream' for streaming output
            
        Returns:
            If override_params contains stream=True, returns a streaming response iterator
            Otherwise, returns the complete response
        """
        return self._generate_common(
            template_name=template_name,
            user_message=user_message,
            input_variables=input_variables,
            verbose=verbose,
            tools=tools,
            use_beta_api=False,
            **override_params
        )

    def generate_beta(
            self,
            template_name: str,
            user_message: Union[str, Dict[str, Any], List[Dict[str, Any]]],
            input_variables: Optional[Dict[str, str]] = None,
            verbose: bool = False,
            tools: Optional[List[Callable]] = None,
            **override_params
    ):
        """Generate a response using beta.parse endpoint.
        
        Args and Returns similar to the generate method, but uses the beta API endpoint.
        """
        return self._generate_common(
            template_name=template_name,
            user_message=user_message,
            input_variables=input_variables,
            verbose=verbose,
            tools=tools,
            use_beta_api=True,
            **override_params
        )
