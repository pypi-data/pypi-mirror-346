#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
使用pytest框架测试markprompt的客户端功能
测试用例涵盖了provider注册和创建功能
"""

import sys
import os
import pytest
from unittest import mock
from typing import Dict, Any

# 添加src目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from markprompt.client import MarkPromptClient
from openai import OpenAI


# 自定义 Mock Provider 类
class MockOpenAIClient:
    """模拟的 OpenAI 客户端类，用于测试自定义 provider"""
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.provider_type = "mock"


# 自定义 provider 工厂函数
def mock_provider_factory(config: Dict[str, Any]):
    """创建模拟的 OpenAI 客户端"""
    return MockOpenAIClient(**config)


@pytest.fixture
def clean_registered_providers():
    """测试前清空所有已注册的 provider"""
    # 保存原始的已注册 provider
    original_providers = MarkPromptClient._registered_providers.copy()
    
    # 清空已注册的 provider
    MarkPromptClient._registered_providers.clear()
    
    yield
    
    # 测试后恢复原始的已注册 provider
    MarkPromptClient._registered_providers.clear()
    MarkPromptClient._registered_providers.update(original_providers)


def test_register_provider(clean_registered_providers):
    """测试注册自定义 provider"""
    # 注册自定义 provider
    MarkPromptClient.register_provider("mock_provider", mock_provider_factory)
    
    # 验证 provider 已被注册
    assert "mock_provider" in MarkPromptClient._registered_providers
    assert MarkPromptClient._registered_providers["mock_provider"] == mock_provider_factory


def test_create_client_from_registered_provider(clean_registered_providers):
    """测试使用注册的 provider 创建客户端"""
    # 注册自定义 provider
    MarkPromptClient.register_provider("mock_provider", mock_provider_factory)
    
    # 创建客户端实例
    client = MarkPromptClient()
    
    # 使用注册的 provider 创建客户端
    provider_config = {
        "name": "mock_provider",  # 指定使用的 provider
        "api_key": "test_key",
        "base_url": "https://test.api.com"
    }
    
    # 创建客户端
    result_client = client._create_client_from_provider(provider_config)
    
    # 验证结果
    assert isinstance(result_client, MockOpenAIClient)
    assert result_client.kwargs["api_key"] == "test_key"
    assert result_client.kwargs["base_url"] == "https://test.api.com"
    assert result_client.provider_type == "mock"


def test_create_client_from_unregistered_provider(clean_registered_providers):
    """测试使用未注册的 provider 创建客户端，应该使用默认的 OpenAI 客户端"""
    # 创建客户端实例
    client = MarkPromptClient()
    
    # 使用未注册的 provider 创建客户端
    provider_config = {
        "name": "unknown_provider",  # 指定使用的 provider
        "api_key": "test_key",
        "base_url": "https://test.api.com"
    }
    
    # 使用 mock 替换 OpenAI 类
    with mock.patch("markprompt.client.OpenAI") as mock_openai:
        # 创建客户端
        client._create_client_from_provider(provider_config)
        
        # 验证结果
        mock_openai.assert_called_once()


def test_create_client_without_provider(clean_registered_providers):
    """测试不指定 provider 创建客户端，应该使用默认的 OpenAI 客户端"""
    # 创建客户端实例
    client = MarkPromptClient()
    
    # 不指定 provider 创建客户端
    provider_config = {
        "api_key": "test_key",
        "base_url": "https://test.api.com"
    }
    
    # 使用 mock 替换 OpenAI 类
    with mock.patch("markprompt.client.OpenAI") as mock_openai:
        # 创建客户端
        client._create_client_from_provider(provider_config)
        
        # 验证结果
        mock_openai.assert_called_once_with(
            api_key="test_key",
            base_url="https://test.api.com"
        )
