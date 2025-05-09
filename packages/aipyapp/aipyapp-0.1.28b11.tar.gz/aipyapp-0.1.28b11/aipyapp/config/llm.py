#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import BaseConfig

PROVIDERS = {
    "TrustToken": {
        "api_base": "https://api.trustoken.cn/v1",
        "models_endpoint": "/models",
        "type": "trust",
        "model": "auto"
    },
    "OpenAI": {
        "api_base": "https://api.openai.com/v1",
        "models_endpoint": "/models",
        "type": "openai"
    },
    "xAI": {
        "api_base": "https://api.x.ai/v1",
        "models_endpoint": "/models",
        "type": "grok"
    },
    "DeepSeek": {
        "api_base": "https://api.deepseek.com",
        "models_endpoint": "/models",
        "type": "deepseek"
    },
    "Gemini": {
        "api_base": "https://generativelanguage.googleapis.com/v1beta/",
        "models_endpoint": "/models",
        "type": "gemini"
    },
    "Claude": {
        "api_base": "https://api.anthropic.com/v1",
        "models_endpoint": "/models",
        "type": "claude"
    }
}

class LLMConfig(BaseConfig):
    FILE = "llm.json"

    def __init__(self, path: str):
        super().__init__(path)
        self.providers = PROVIDERS

    def need_config(self):
        """检查是否需要配置LLM。
        """
        if not self.config:
            return True
        
        for _, config in self.config.items() :
            if config.get("enable", True):
                return False
        return True
