"""
MarkPrompt template parser.
"""
import logging
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Union, Any, Optional

from .logger import setup_logger

import frontmatter

from .models import PromptTemplate

logger = setup_logger(__name__)

DEFAULT_PROVIDER = "openai"


class TemplateParser:
    """Parser for MarkPrompt templates."""

    # 基本角色定义
    BASIC_ROLES = {
        "system": "system\n---\n",
        "user": "user\n---\n",
        "assistant": "assistant\n---\n"
    }

    # 用户子类型定义 - 使用完整的角色标识符作为键
    USER_SUBTYPES = {
        "user.text": "user.text\n---\n",
        "user.image_url": "user.image_url\n---\n"
    }

    # 合并所有角色为完整的角色字典
    @property
    def DEFAULT_ROLES(self):
        roles = self.BASIC_ROLES.copy()
        roles.update(self.USER_SUBTYPES)  # 直接添加子类型，无需修改键
        return roles

    def __init__(self):
        self._var_pattern = re.compile(r"{{([a-z_]+)}}")

    def _process_response_format(self, response_format, template_dir) -> Dict[str, Any]:
        """处理response_format字段。如果是字符串类型，则将其视为JSON文件路径读取并解析。
        
        Args:
            response_format: 可能是字符串文件路径或已经是字典的response_format
            template_dir: 模板目录路径，文件将用此路径来解析相对路径
            
        Returns:
            解析后的response_format字典，如果解析失败则抛出异常
        """
        # 如果不是字符串，直接返回原值
        if not isinstance(response_format, str):
            return response_format
            
        try:
            # 仅尝试最直接的解析方式 - 基于模板目录
            file_path = template_dir / response_format
            logger.info(f"_process_response_format template_dir: {self.template_dir}")
            logger.info(f"_process_response_format response_format: {self.response_format}")
            
            # 如果路径包含模板目录名称，则尝试去除这一部分
            if '/'.join(template_dir.parts[-1:]) in response_format:
                # 仅获取目录名之后的路径部分
                dir_name = template_dir.name
                if response_format.startswith(dir_name + '/'):
                    rel_path = response_format[len(dir_name)+1:]
                    file_path = template_dir / rel_path
            
            logger.info(f"Load response_format json config file: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                json_content = f.read()
                return json.loads(json_content)
                
        except FileNotFoundError:
            raise ValueError(f"无法找到文件: {file_path}\n配置路径: {response_format}")
        except json.JSONDecodeError as e:
            raise ValueError(f"解析JSON失败: {file_path}, 错误: {e}")
        except Exception as e:
            raise ValueError(f"处理出错: {file_path}, 错误: {e}")
                


    def parse(self, content: str, template_dir = None) -> PromptTemplate:
        """Parse template content into a PromptTemplate object.
        
        Args:
            content: 模板文件内容
            template_dir: 模板目录路径，用于解析response_format的相对路径
        """
        metadata, template_content = self._parse_frontmatter(content)

        # 获取角色定义（现在DEFAULT_ROLES是一个属性方法）
        roles = self.DEFAULT_ROLES
        if "roles" in metadata:
            # 创建一个副本再更新，避免修改原始属性
            roles = roles.copy()
            roles.update(metadata["roles"])

        messages = self._parse_messages(template_content, roles)

        # 处理generation_config中的response_format字段
        if "generation_config" in metadata and "response_format" in metadata["generation_config"]:
            response_format = metadata["generation_config"]["response_format"]
            # 使用简化后的调用方式，只传递template_dir参数
            metadata["generation_config"]["response_format"] = self._process_response_format(
                response_format,
                template_dir=template_dir
            )

        provider_config = None
        if "provider" in metadata:
            provider_config = metadata.get("provider")
        elif "generation_config" in metadata and "model" in metadata["generation_config"]:
            model = metadata["generation_config"]["model"]
            parsed_model = self._parse_model_string(model)

            if parsed_model["provider"] != model:  # 表示成功解析了 provider/model 格式
                metadata["generation_config"]["model"] = parsed_model["model"]
                provider_config = {"name": parsed_model["provider"]}

        template = PromptTemplate(
            metadata=metadata.get("metadata"),
            roles=roles,
            generation_config=metadata.get("generation_config", {}),
            input_variables=metadata.get("input_variables", {}),
            messages=messages,
            provider=provider_config
        )
        return template

    def _parse_model_string(self, model_string: str) -> Dict[str, str]:
        """Parse model string in format 'provider/model'."""
        if "/" in model_string:
            provider_name, model_name = model_string.split("/", 1)
            return {
                "provider": provider_name,
                "model": model_name
            }
        return {
            "provider": DEFAULT_PROVIDER,
            "model": model_string
        }

    # 移除不再需要的辅助方法，因为现在使用正则表达式实现解析
    def _parse_user_subtype_content(self, subtype: str, content: str) -> Dict[str, Any]:
        """解析用户子类型的内容。"""
        if subtype == "text":
            return {
                "type": "text",
                "text": content
            }
        elif subtype == "image_url":
            # 先尝试将内容解析为 YAML
            content_stripped = content.strip()
            try:
                import yaml
                image_data = yaml.safe_load(content_stripped)

                # 检查解析后的内容是否为字典格式且包含 url
                if isinstance(image_data, dict) and ("url" in image_data):
                    return {
                        "type": "image_url",
                        "image_url": image_data
                    }
            except Exception as e:
                # YAML 解析失败时，会继续往下执行
                logger.debug(f"Failed to parse image_url content as YAML，return as url")

            # 如果不是有效的 YAML 或解析失败，将内容直接作为 URL
            return {
                "type": "image_url",
                "image_url": {
                    "url": content_stripped
                }
            }

        # 未知子类型时默认处理为文本
        logger.warning(f"Unknown user subtype: {subtype}, treating as text")
        return {
            "type": "text",
            "text": content
        }

    def _parse_messages(self, content: str, roles: Dict[str, str]) -> List[Dict[str, Union[str, List[Dict[str, Any]]]]]:
        """按照分块、解析、组装的方式处理模板内容。"""
        # 如果没有角色定义，则视为系统消息
        if not roles:
            return [{"role": "system", "content": content.strip()}]

        # 第一阶段: 按角色类型分块
        blocks = self._split_content_into_blocks(content, roles)
        if not blocks:
            return [{"role": "system", "content": content.strip()}]

        # 第二阶段: 分析块并组建消息
        return self._build_messages_from_blocks(blocks)

    def _split_content_into_blocks(self, content: str, roles: Dict[str, str]) -> List[Dict[str, str]]:
        """将内容按角色标记分割为多个块。
        
        每个块都包含 type (角色ID) 和 content (内容)。
        """
        # 创建角色标记映射
        marker_to_role_id = {}
        for role_id, format_str in roles.items():
            marker = format_str.split('\n')[0]
            marker_to_role_id[marker.lower()] = role_id

        # 使用正则表达式切分内容
        markers = [re.escape(marker) for marker in marker_to_role_id.keys()]
        pattern = r"(^|\n)(" + "|".join(markers) + r")\n---\n"
        regex = re.compile(pattern, re.IGNORECASE)

        matches = list(regex.finditer(content))
        if not matches:
            return []

        # 提取块
        blocks = []
        for i, match in enumerate(matches):
            marker = match.group(2).lower()
            role_id = marker_to_role_id.get(marker)
            if not role_id:
                continue

            start_pos = match.end()
            end_pos = len(content) if i == len(matches) - 1 else matches[i + 1].start()
            block_content = content[start_pos:end_pos].strip()

            blocks.append({
                "type": role_id,  # 存储角色ID作为类型
                "content": block_content
            })

        return blocks

    def _build_messages_from_blocks(self, blocks: List[Dict[str, str]]) -> List[
        Dict[str, Union[str, List[Dict[str, Any]]]]]:
        """根据块构建消息列表。
        
        只有连续的user.xxx内容才会被合并在一起，如果中间插入了其他的类型，则是单独分开的消息。
        """
        messages = []
        current_user_blocks = []  # 当前正在处理的连续用户块

        # 处理所有块
        for i, block in enumerate(blocks):
            block_type = block["type"]
            block_content = block["content"]

            # 处理用户相关类型
            if block_type == "user" or block_type.startswith("user."):
                # 将当前块添加到连续用户块列表
                current_user_blocks.append(block)
            else:
                # 如果有未处理的用户块，先处理它们
                if current_user_blocks:
                    user_parts = self._process_user_blocks(current_user_blocks)
                    if user_parts:
                        messages.append({
                            "role": "user",
                            "content": user_parts
                        })
                    current_user_blocks = []

                # 添加非用户类型的消息
                messages.append({
                    "role": block_type,
                    "content": block_content
                })

        # 处理最后的用户块
        if current_user_blocks:
            user_parts = self._process_user_blocks(current_user_blocks)
            if user_parts:
                messages.append({
                    "role": "user",
                    "content": user_parts
                })

        return messages

    def _process_user_blocks(self, user_blocks: List[Dict[str, str]]) -> Union[str, List[Dict[str, Any]]]:
        """处理用户块，包括普通用户内容和用户子类型。
        
        返回:
            - 如果只有一个普通用户块 ("user") 且没有子类型块，则返回其内容作为字符串
            - 如果有多个块或包含子类型，则返回结构化数组
        """
        # 检查是否只有一个普通用户块
        if len(user_blocks) == 1 and user_blocks[0]["type"] == "user":
            # 如果只有一个普通用户块，直接返回其内容作为字符串
            return user_blocks[0]["content"]

        # 如果有多个块或不仅仅是用户块，则处理为结构化内容
        user_parts = []

        for block in user_blocks:
            block_type = block["type"]
            block_content = block["content"]

            if block_type == "user":
                # 普通用户消息作为文本处理
                user_parts.append({
                    "type": "text",
                    "text": block_content
                })
            elif block_type.startswith("user."):
                # 提取子类型
                subtype = block_type.split(".")[1]
                processed_part = self._parse_user_subtype_content(subtype, block_content)
                user_parts.append(processed_part)

        return user_parts

    def render(self, template: PromptTemplate, input_values: Optional[Dict[str, str]] = None) -> List[
        Dict[str, Union[str, List[Dict[str, Any]]]]]:
        """根据输入变量渲染模板消息。"""
        variables = {}
        if template.input_variables:
            variables.update(template.input_variables)
        if input_values:
            variables.update(input_values)

        rendered_messages = []
        for message in template.messages:
            rendered_content = self._replace_variables(message["content"], variables)
            rendered_messages.append({
                "role": message["role"],
                "content": rendered_content
            })

        return rendered_messages

    def _replace_variables(self, content: Union[str, List[Dict[str, Any]]], variables: Dict[str, str]) -> Union[
        str, List[Dict[str, Any]]]:
        """Replace variables in content with their Jinja2."""
        from jinja2 import Template, TemplateSyntaxError

        # 如果内容是列表（复杂消息结构），逐个处理每个部分
        if isinstance(content, list):
            result = []
            for item in content:
                processed_item = dict(item)  # 创建副本以避免修改原始数据

                # 处理文本部分
                if item.get("type") == "text" and isinstance(item.get("text"), str):
                    try:
                        template = Template(item["text"])
                        processed_item["text"] = template.render(**variables)
                    except TemplateSyntaxError as e:
                        logger.warning(f"模板语法错误 (text): {e}")

                # 处理图片URL部分（处理所有字段，包括 url 和 detail 等配置参数）
                elif item.get("type") == "image_url" and isinstance(item.get("image_url"), dict):
                    image_url = item["image_url"]
                    processed_item["image_url"] = dict(image_url)  # 创建副本

                    # 处理 image_url 字典中的所有字符串字段
                    for key, value in image_url.items():
                        if isinstance(value, str):
                            try:
                                template = Template(value)
                                processed_item["image_url"][key] = template.render(**variables)
                            except TemplateSyntaxError as e:
                                logger.warning(f"模板语法错误 (image_url.{key}): {e}")

                result.append(processed_item)
            return result

        # 如果是普通字符串，按原来方式处理
        try:
            template = Template(content)
            return template.render(**variables)
        except TemplateSyntaxError as e:
            logger.warning(f"模板语法错误: {e}")
            return content

    def _parse_frontmatter(self, content: str) -> Tuple[dict, str]:
        """Parse frontmatter and content."""
        try:
            post = frontmatter.loads(content)
            if not post.metadata:
                raise ValueError("No metadata found in template")
            return post.metadata, post.content.strip()
        except Exception as e:
            raise ValueError(f"Invalid frontmatter: {e}")
