"""
Configuration Module

Provides configuration management for the video generation app.
"""

from .gemini_config import GeminiConfig, get_system_prompt
from .veo_config import VeoConfig, build_veo_prompt
from .templates import (
    VideoTemplate,
    get_template_by_id,
    get_templates_by_type,
    list_all_templates,
    SALES_TEMPLATES,
    SERVICE_TEMPLATES,
)

__all__ = [
    "GeminiConfig",
    "get_system_prompt",
    "VeoConfig",
    "build_veo_prompt",
    "VideoTemplate",
    "get_template_by_id",
    "get_templates_by_type",
    "list_all_templates",
    "SALES_TEMPLATES",
    "SERVICE_TEMPLATES",
]
