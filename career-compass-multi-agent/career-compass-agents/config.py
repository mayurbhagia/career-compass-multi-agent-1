
import os
from typing import Optional

class AgentConfig:
    """Configuration for Career Guidance Agent"""
    
    # AWS Configuration
    AWS_REGION: str = os.getenv("AWS_REGION", "us-west-2")
    
    # Bedrock Configuration
    BEDROCK_MODEL_ID: str = "us.amazon.nova-pro-v1:0"
    BEDROCK_MODEL_ARN: str = f"arn:aws:bedrock:{AWS_REGION}::foundation-model/{BEDROCK_MODEL_ID}"
    
    # Knowledge Base Configuration
    KNOWLEDGE_BASE_ID: str = os.getenv("KB_ID", "")
    
    # Agent Configuration
    AGENT_NAME: str = "CareerGuidanceAgent"
    AGENT_DESCRIPTION: str = "AI agent that provides career guidance using knowledge base"
    
    # Temperature and inference parameters
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2000
    TOP_P: float = 0.9
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.KNOWLEDGE_BASE_ID:
            raise ValueError("KNOWLEDGE_BASE_ID must be set in environment variables")
        return True