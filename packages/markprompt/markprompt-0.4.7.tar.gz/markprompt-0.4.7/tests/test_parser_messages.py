#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
使用pytest框架测试markprompt扩展的markdown解析功能
测试用例涵盖了user.text和user.image_url的解析及变量替换
"""

import sys
import os
import re
import pytest
from unittest import mock
import yaml
from markprompt.core import TemplateParser

# 添加src目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  



# 定义pytest测试函数

@pytest.fixture
def template_parser():
    """返回TemplateParser实例"""
    return TemplateParser()


def test_basic_parsing(template_parser):
    """测试基本的消息解析功能"""
    # 不缩进模板内容，保持原始格式
    template_content = """
system
---
you are a helpful assistant.

user
---
hello

assistant
---
hi
""".strip()

    messages = template_parser._parse_messages(template_content, template_parser.DEFAULT_ROLES)
    
    assert len(messages) == 3
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == "you are a helpful assistant."
    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == "hello"
    assert messages[2]["role"] == "assistant"
    assert messages[2]["content"] == "hi"


def test_complex_user_message_yaml_format(template_parser):
    """测试复杂的用户消息格式 - 带YAML格式的image_url"""
    # 不缩进模板内容，并使用正确的YAML格式
    template_content = """system
---
you are a helpful assistant.

user.text
---
What is in this image?

user.image_url
---
url: https://upload.wikimedia.org/commons/nature-boardwalk.jpg
detail: low

assistant
---
图片中有自然步道"""
    messages = template_parser._parse_messages(template_content, template_parser.DEFAULT_ROLES)
    print(messages)
    
    # 验证基本结构
    assert len(messages) == 3
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == "you are a helpful assistant."
    assert messages[1]["role"] == "user"
    assert messages[2]["role"] == "assistant"
    assert messages[2]["content"] == "图片中有自然步道"

    
    # 验证复杂的用户消息结构
    user_content = messages[1]["content"]
    assert isinstance(user_content, list)
    assert len(user_content) == 2
    
    # 验证文本部分
    assert user_content[0]["type"] == "text"
    assert user_content[0]["text"] == "What is in this image?"
    
    # 验证图像URL部分
    assert user_content[1]["type"] == "image_url"
    assert user_content[1]["image_url"]["url"] == "https://upload.wikimedia.org/commons/nature-boardwalk.jpg"
    assert user_content[1]["image_url"]["detail"] == "low"


def test_complex_user_message_simple_format(template_parser):
    """测试复杂的用户消息格式 - 简单URL格式"""
    template_content = """
system
---
you are a helpful assistant.

user.text
---
What is in this image?

user.image_url
---
https://upload.wikimedia.org/commons/nature-boardwalk.jpg

assistant
---
图片中有自然步道
""".strip()
    messages = template_parser._parse_messages(template_content, template_parser.DEFAULT_ROLES)
    
    # 验证基本结构
    assert len(messages) == 3
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == "you are a helpful assistant."
    assert messages[1]["role"] == "user"
    assert messages[2]["role"] == "assistant"
    
    # 验证复杂的用户消息结构
    user_content = messages[1]["content"]
    assert isinstance(user_content, list)
    assert len(user_content) == 2
    
    # 验证文本部分
    assert user_content[0]["type"] == "text"
    assert user_content[0]["text"] == "What is in this image?"
    
    # 验证图像URL部分(简单格式)
    assert user_content[1]["type"] == "image_url"
    assert user_content[1]["image_url"]["url"] == "https://upload.wikimedia.org/commons/nature-boardwalk.jpg"


def test_multiple_user_parts(template_parser):
    """测试多个用户部分，包含多个图像"""
    # 不缩进模板内容，并使用正确的YAML格式
    template_content = """system
---
you are a helpful assistant.

user.text
---
What is the difference between these two images?

user.image_url
---
url: https://upload.wikimedia.org/commons/nature-boardwalk.jpg
detail: high

user.text
---
And this one:

user.image_url
---
https://upload.wikimedia.org/commons/city-skyline.jpg

assistant
---
第一张图片是自然步道，第二张图片是城市天际线。"""
    messages = template_parser._parse_messages(template_content, template_parser.DEFAULT_ROLES)
    
    # 验证基本结构
    assert len(messages) == 3
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == "you are a helpful assistant."
    assert messages[1]["role"] == "user"
    assert messages[2]["role"] == "assistant"
    assert messages[2]["content"] == "第一张图片是自然步道，第二张图片是城市天际线。"
    
    # 验证复杂的用户消息结构
    user_content = messages[1]["content"]
    assert isinstance(user_content, list)
    assert len(user_content) == 4
    
    # 验证第一个文本部分
    assert user_content[0]["type"] == "text"
    assert user_content[0]["text"] == "What is the difference between these two images?"
    
    # 验证第一个图像URL
    assert user_content[1]["type"] == "image_url"
    assert user_content[1]["image_url"]["url"] == "https://upload.wikimedia.org/commons/nature-boardwalk.jpg"
    assert user_content[1]["image_url"]["detail"] == "high"
    
    # 验证第二个文本部分
    assert user_content[2]["type"] == "text"
    assert user_content[2]["text"] == "And this one:"
    
    # 验证第二个图像URL
    assert user_content[3]["type"] == "image_url"
    assert user_content[3]["image_url"]["url"] == "https://upload.wikimedia.org/commons/city-skyline.jpg"


def test_continuous_vs_noncontinuous_user_blocks(template_parser):
    """测试连续与非连续的user.xxx类型处理"""
    template_content = """system
---
you are a helpful assistant.

user.text
---
Here is the first image:

user.image_url
---
url: https://example.com/image1.jpg
detail: high

system
---
This is a system message in between user blocks.

user.text
---
Here is the second image:

user.image_url
---
url: https://example.com/image2.jpg
detail: low

assistant
---
I see both images."""

    messages = template_parser._parse_messages(template_content, template_parser.DEFAULT_ROLES)
    
    # 应该有5个消息: system, user(组1), system, user(组2), assistant
    assert len(messages) == 5
    
    # 验证第一个系统消息
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == "you are a helpful assistant."
    
    # 验证第一组用户消息 (连续的user.text和user.image_url)
    assert messages[1]["role"] == "user"
    user_content1 = messages[1]["content"]
    assert isinstance(user_content1, list)
    assert len(user_content1) == 2
    assert user_content1[0]["type"] == "text"
    assert user_content1[0]["text"] == "Here is the first image:"
    assert user_content1[1]["type"] == "image_url"
    assert user_content1[1]["image_url"]["url"] == "https://example.com/image1.jpg"
    assert user_content1[1]["image_url"]["detail"] == "high"
    
    # 验证中间的系统消息
    assert messages[2]["role"] == "system"
    assert messages[2]["content"] == "This is a system message in between user blocks."
    
    # 验证第二组用户消息 (另一组连续的user.text和user.image_url)
    assert messages[3]["role"] == "user"
    user_content2 = messages[3]["content"]
    assert isinstance(user_content2, list)
    assert len(user_content2) == 2
    assert user_content2[0]["type"] == "text"
    assert user_content2[0]["text"] == "Here is the second image:"
    assert user_content2[1]["type"] == "image_url"
    assert user_content2[1]["image_url"]["url"] == "https://example.com/image2.jpg"
    assert user_content2[1]["image_url"]["detail"] == "low"
    
    # 验证助手消息
    assert messages[4]["role"] == "assistant"
    assert messages[4]["content"] == "I see both images."


def test_variable_replacement(template_parser):
    """测试变量替换功能"""
    # 测试 1: 简单文本替换
    text_content = "Hello {{name}}, I see..."
    variables = {"name": "张三"}
    expected_result = "Hello 张三, I see..."
    
    # 直接调用 _replace_variables 方法
    result1 = template_parser._replace_variables(text_content, variables)
    assert result1 == expected_result
    
    # 测试 2: 复杂对象结构替换
    complex_content = [
        {"type": "text", "text": "My name is {{name}}. What is in this image?"},
        {"type": "image_url", "image_url": {"url": "{{image_url}}", "detail": "{{detail_level}}"}}
    ]
    
    complex_variables = {
        "name": "张三",
        "image_url": "https://example.com/test.jpg",
        "detail_level": "auto"
    }
    
    # 直接调用 _replace_variables 方法处理复杂对象
    result2 = template_parser._replace_variables(complex_content, complex_variables)
    
    # 验证复杂结果
    assert isinstance(result2, list)
    assert len(result2) == 2
    assert result2[0]["type"] == "text"
    assert result2[0]["text"] == "My name is 张三. What is in this image?"
    assert result2[1]["type"] == "image_url"
    assert result2[1]["image_url"]["url"] == "https://example.com/test.jpg"
    assert result2[1]["image_url"]["detail"] == "auto"
    

