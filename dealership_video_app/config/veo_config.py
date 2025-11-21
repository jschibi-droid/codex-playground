"""
Veo Video Generation Configuration Module

Handles configuration for Google's Veo video generation API.
"""

import os
from dataclasses import dataclass
from typing import Literal, Optional


VideoQuality = Literal["low", "medium", "high", "ultra"]
VideoStyle = Literal["professional", "dynamic", "friendly", "luxury", "casual"]


@dataclass
class VeoConfig:
    """Configuration for Veo video generation API"""
    
    api_key: str
    model_name: str = "veo-001"
    default_duration: int = 30  # seconds
    default_quality: VideoQuality = "high"
    default_style: VideoStyle = "professional"
    max_duration: int = 60  # seconds
    timeout: int = 300  # seconds
    
    @classmethod
    def from_env(cls) -> "VeoConfig":
        """Create configuration from environment variables"""
        api_key = os.getenv("VEO_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "VEO_API_KEY or GEMINI_API_KEY not found. "
                "Please set it in your environment or .env file."
            )
        
        return cls(
            api_key=api_key,
            model_name=os.getenv("VEO_MODEL", "veo-001"),
            default_duration=int(os.getenv("DEFAULT_VIDEO_DURATION", "30")),
            default_quality=os.getenv("DEFAULT_VIDEO_QUALITY", "high"),  # type: ignore
            max_duration=int(os.getenv("MAX_VIDEO_DURATION", "60")),
        )


# Video generation parameters presets
QUALITY_PRESETS = {
    "low": {
        "resolution": "480p",
        "fps": 24,
        "bitrate": "1000k",
    },
    "medium": {
        "resolution": "720p",
        "fps": 30,
        "bitrate": "2500k",
    },
    "high": {
        "resolution": "1080p",
        "fps": 30,
        "bitrate": "5000k",
    },
    "ultra": {
        "resolution": "4k",
        "fps": 60,
        "bitrate": "10000k",
    },
}


STYLE_PRESETS = {
    "professional": {
        "description": "Clean, polished, corporate feel with smooth camera movements",
        "camera_style": "smooth pans and slow zooms",
        "lighting": "bright, even, professional lighting",
        "color_grading": "neutral with slight saturation boost",
        "pacing": "steady and measured",
    },
    "dynamic": {
        "description": "Energetic, fast-paced with dynamic camera movements",
        "camera_style": "quick cuts, dynamic angles, tracking shots",
        "lighting": "dramatic with high contrast",
        "color_grading": "vibrant and saturated",
        "pacing": "fast and exciting",
    },
    "friendly": {
        "description": "Warm, approachable, family-oriented feel",
        "camera_style": "gentle movements, welcoming angles",
        "lighting": "warm, natural, inviting",
        "color_grading": "warm tones, soft contrast",
        "pacing": "relaxed and comfortable",
    },
    "luxury": {
        "description": "Premium, sophisticated, high-end presentation",
        "camera_style": "elegant slow pans, reveal shots",
        "lighting": "sophisticated with dramatic shadows",
        "color_grading": "rich, deep tones with high contrast",
        "pacing": "slow and deliberate",
    },
    "casual": {
        "description": "Relaxed, everyday, down-to-earth feel",
        "camera_style": "handheld feel, natural movements",
        "lighting": "natural, realistic lighting",
        "color_grading": "natural, minimal processing",
        "pacing": "moderate and natural",
    },
}


# Prompt template for Veo
VEO_PROMPT_TEMPLATE = """
[VIDEO TYPE]: {video_type}
[DURATION]: {duration} seconds
[STYLE]: {style}
[QUALITY]: {quality}

SCENE DESCRIPTION:
{scene_description}

FOCUS ELEMENTS:
{focus_elements}

VISUAL DETAILS:
- Camera: {camera_movements}
- Lighting: {lighting}
- Environment: {environment}
- Color Grading: {color_grading}

TEXT OVERLAYS:
{text_overlays}

BRAND ELEMENTS:
{brand_elements}

MOOD & PACING:
{mood_pacing}

AUDIO DIRECTION:
{audio_direction}
"""


def build_veo_prompt(
    video_type: str,
    duration: int,
    style: VideoStyle,
    quality: VideoQuality,
    scene_description: str,
    focus_elements: str,
    text_overlays: str,
    brand_elements: str = "Standard dealership branding",
    environment: str = "Modern car dealership showroom",
    audio_direction: str = "Upbeat background music, professional voiceover",
) -> str:
    """Build a structured prompt for Veo video generation"""
    
    style_preset = STYLE_PRESETS.get(style, STYLE_PRESETS["professional"])
    quality_preset = QUALITY_PRESETS.get(quality, QUALITY_PRESETS["high"])
    
    return VEO_PROMPT_TEMPLATE.format(
        video_type=video_type,
        duration=duration,
        style=style,
        quality=quality,
        scene_description=scene_description,
        focus_elements=focus_elements,
        camera_movements=style_preset["camera_style"],
        lighting=style_preset["lighting"],
        environment=environment,
        color_grading=style_preset["color_grading"],
        text_overlays=text_overlays,
        brand_elements=brand_elements,
        mood_pacing=f"{style_preset['description']} - {style_preset['pacing']} pacing",
        audio_direction=audio_direction,
    ).strip()
