import litellm
from typing import Any, Dict, List, Optional
from loguru import logger

class LLMManager:
    """
    Unified interface for multiple LLM providers using LiteLLM.
    Supports Kimi, Qwen, Mistral, Llama, DeepSeek, etc.
    """
    def __init__(self, default_model: str = "gpt-4o"):
        self.default_model = default_model
        litellm.drop_params = True # Drop unsupported params for different providers

    async def completion(
        self, 
        messages: List[Dict[str, str]], 
        model: Optional[str] = None,
        **kwargs
    ) -> Any:
        target_model = model or self.default_model
        try:
            logger.info(f"Calling LLM: {target_model}")
            response = await litellm.acompletion(
                model=target_model,
                messages=messages,
                **kwargs
            )
            return response
        except Exception as e:
            logger.error(f"Error calling LLM {target_model}: {str(e)}")
            raise e

    def get_supported_models(self) -> List[str]:
        # This can be expanded based on LiteLLM's supported list
        return [
            "moonshot/moonshot-v1-8k", # Kimi
            "qwen/qwen-max",           # Qwen
            "mistral/mistral-large-latest",
            "deepseek/deepseek-chat",
            "zhipu/glm-4",
            "minimax/abab6.5-chat",
            "groq/llama3-70b-8192"
        ]
