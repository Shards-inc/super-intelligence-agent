import pytest
from core.llm_manager import LLMManager

def test_llm_manager_init():
    manager = LLMManager(default_model="gpt-4o")
    assert manager.default_model == "gpt-4o"

def test_supported_models():
    manager = LLMManager()
    models = manager.get_supported_models()
    assert "deepseek/deepseek-chat" in models
    assert "moonshot/moonshot-v1-8k" in models
