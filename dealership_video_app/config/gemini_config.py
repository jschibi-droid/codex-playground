"""
Gemini 3.0 Configuration Module

Handles configuration and initialization for Google's Gemini AI model.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class GeminiConfig:
    """Configuration for Gemini 3.0 API"""
    
    api_key: str
    model_name: str = "gemini-3.0-pro"
    temperature: float = 0.7
    max_output_tokens: int = 2048
    top_p: float = 0.9
    top_k: int = 40
    
    @classmethod
    def from_env(cls) -> "GeminiConfig":
        """Create configuration from environment variables"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Please set it in your environment or .env file."
            )
        
        return cls(
            api_key=api_key,
            model_name=os.getenv("GEMINI_MODEL", "gemini-3.0-pro"),
            temperature=float(os.getenv("GEMINI_TEMPERATURE", "0.7")),
            max_output_tokens=int(os.getenv("GEMINI_MAX_TOKENS", "2048")),
        )
    
    def get_generation_config(self) -> dict:
        """Get generation configuration for Gemini API"""
        return {
            "temperature": self.temperature,
            "max_output_tokens": self.max_output_tokens,
            "top_p": self.top_p,
            "top_k": self.top_k,
        }


# System prompts for different conversation stages
SYSTEM_PROMPTS = {
    "initial": """You are an expert video production assistant for car dealerships. 
Your role is to help create professional video content for either sales or service advertising.

Be conversational, helpful, and ask clarifying questions to understand the user's needs.
Guide them through the video creation process step by step.""",
    
    "sales_focused": """You are helping create a sales-focused video for a car dealership.
Focus on:
- Vehicle features and benefits
- Pricing and financing offers
- Inventory availability
- Call-to-action for test drives or purchases
- Creating excitement and urgency

Ask about specific vehicles, target audience, promotional offers, and desired tone.""",
    
    "service_focused": """You are helping create a service-focused video for a car dealership.
Focus on:
- Service offerings and packages
- Maintenance benefits
- Convenience and expertise
- Customer trust and satisfaction
- Call-to-action for scheduling service

Ask about specific services, seasonal offers, target concerns, and desired tone.""",
    
    "prompt_generation": """Based on the conversation, generate a detailed video generation prompt for Veo.
Include:
- Video type and duration
- Scene descriptions
- Visual elements (camera movements, lighting, environment)
- Text overlays (headlines, details, call-to-action)
- Brand elements (colors, logos)
- Mood and tone
- Specific vehicles or services to highlight

Format the prompt in a structured way that Veo can understand.""",
    
    "customization": """You are helping customize an existing video.
Analyze what the user wants to change and provide specific modification instructions.
Focus on:
- What elements to keep vs. change
- New content to add
- Visual style adjustments
- Text/overlay updates
- Timing and pacing modifications"""
}


def get_system_prompt(stage: str) -> str:
    """Get appropriate system prompt for conversation stage"""
    return SYSTEM_PROMPTS.get(stage, SYSTEM_PROMPTS["initial"])
