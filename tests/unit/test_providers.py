from core.providers import get_provider_for_model

def test_get_provider_for_model():
    assert get_provider_for_model("moonshot-v1-8k") == "kimi"
    assert get_provider_for_model("deepseek-chat") == "deepseek"
    assert get_provider_for_model("qwen-max") == "qwen"
    assert get_provider_for_model("unknown-model") == "openai"
