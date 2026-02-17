from typing import Dict, Any

PROVIDERS_CONFIG: Dict[str, Dict[str, Any]] = {
    "kimi": {
        "base_url": "https://api.moonshot.cn/v1",
        "env_key": "MOONSHOT_API_KEY",
        "models": ["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"]
    },
    "deepseek": {
        "base_url": "https://api.deepseek.com",
        "env_key": "DEEPSEEK_API_KEY",
        "models": ["deepseek-chat", "deepseek-coder"]
    },
    "zhipu": {
        "base_url": "https://open.bigmodel.cn/api/paas/v4/",
        "env_key": "ZHIPU_API_KEY",
        "models": ["glm-4", "glm-4v", "glm-3-turbo"]
    },
    "qwen": {
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "env_key": "DASHSCOPE_API_KEY",
        "models": ["qwen-turbo", "qwen-plus", "qwen-max"]
    },
    "mistral": {
        "base_url": "https://api.mistral.ai/v1",
        "env_key": "MISTRAL_API_KEY",
        "models": ["mistral-tiny", "mistral-small", "mistral-medium", "mistral-large-latest"]
    }
}

def get_provider_for_model(model_name: str) -> str:
    for provider, config in PROVIDERS_CONFIG.items():
        if any(m in model_name for m in config["models"]):
            return provider
    return "openai" # Default fallback
