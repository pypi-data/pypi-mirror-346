from dataclasses import dataclass
from enum import Enum
from typing import Dict

class ModelProvider(Enum):
    OPENAI = "openai"
    GOOGLE = "google"
    ANTHROPIC = "anthropic"

# Map provider strings to ModelProvider enum values
PROVIDER_MAP: Dict[str, ModelProvider] = {
    "openai": ModelProvider.OPENAI,
    "google": ModelProvider.GOOGLE,
    "anthropic": ModelProvider.ANTHROPIC
}

@dataclass(frozen=True)
class LLMConfig:
    """Configuration for the language model feature."""
    model_config_name: str = "openai/gpt-4o"
    temperature: float = 0.7

    def get_model_provider(self) -> ModelProvider:
        """
        Determines the appropriate provider based on the model_config_name.
        
        Returns:
            ModelProvider: The determined provider for the model.
        
        Raises:
            ValueError: If the model provider cannot be determined from the model_config_name.
        """
        provider_part = self.model_config_name.split('/')[0].lower()
        if provider_part in PROVIDER_MAP:
            return PROVIDER_MAP[provider_part]
        raise ValueError(f"Unknown model provider: {self.model_config_name}. Cannot determine the appropriate API provider.") 

    def get_model_name(self) -> str:
        """
        Returns the model name from the model_config_name.
        
        Returns:
            str: The model name.
        """
        return self.model_config_name.split('/')[1]