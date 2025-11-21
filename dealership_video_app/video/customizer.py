"""
Video Customizer

Handles video customization and modification based on user requests.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class CustomizationRequest:
    """Request for video customization"""
    source_video_path: str
    modifications: List[Dict[str, Any]]
    preserve_audio: bool = True
    preserve_timing: bool = True
    output_format: str = "mp4"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "source_video_path": self.source_video_path,
            "modifications": self.modifications,
            "preserve_audio": self.preserve_audio,
            "preserve_timing": self.preserve_timing,
            "output_format": self.output_format,
        }


class VideoCustomizer:
    """
    Handles video customization operations
    
    Takes existing videos and modifies them based on user requirements,
    such as updating text, changing colors, replacing elements, etc.
    """
    
    def __init__(self, veo_client: Optional[Any] = None):
        """
        Initialize video customizer
        
        Args:
            veo_client: Optional VeoVideoGenerator client
        """
        self.veo_client = veo_client
    
    def customize(
        self,
        source_video_path: str,
        modifications: List[Dict[str, Any]],
        output_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Apply customizations to video
        
        Args:
            source_video_path: Path to source video
            modifications: List of modification instructions
            output_path: Optional output path
            
        Returns:
            Result with customized video path/URL
        """
        # Build customization prompt
        customization_prompt = self._build_customization_prompt(
            modifications
        )
        
        # Apply customizations using Veo
        if self.veo_client:
            result = self.veo_client.customize_existing(
                source_video_path=source_video_path,
                modifications={
                    "prompt": customization_prompt,
                    "modifications": modifications,
                },
                output_path=output_path,
            )
            
            return {
                "success": result.success,
                "video_url": result.video_url,
                "video_path": result.video_path,
                "error": result.error_message,
            }
        
        # Mock response if no client available
        return {
            "success": True,
            "video_url": "https://example.com/customized_video.mp4",
            "video_path": output_path,
            "modifications_applied": len(modifications),
        }
    
    def _build_customization_prompt(
        self,
        modifications: List[Dict[str, Any]]
    ) -> str:
        """
        Build a detailed customization prompt
        
        Args:
            modifications: List of modification instructions
            
        Returns:
            Formatted customization prompt
        """
        prompt_parts = ["Apply the following modifications to the video:\n"]
        
        for i, mod in enumerate(modifications, 1):
            mod_type = mod.get("type", "general")
            
            if mod_type == "replace_text":
                old_text = mod.get("old_text", "")
                new_text = mod.get("new_text", "")
                prompt_parts.append(
                    f"{i}. Replace text '{old_text}' with '{new_text}'"
                )
            
            elif mod_type == "update_pricing":
                new_price = mod.get("price", "")
                prompt_parts.append(
                    f"{i}. Update pricing information to '{new_price}'"
                )
            
            elif mod_type == "change_vehicle":
                vehicle = mod.get("vehicle", "")
                prompt_parts.append(
                    f"{i}. Replace featured vehicle with {vehicle}"
                )
            
            elif mod_type == "change_style":
                style = mod.get("style", "")
                prompt_parts.append(
                    f"{i}. Modify visual style to be more {style}"
                )
            
            elif mod_type == "add_overlay":
                overlay_text = mod.get("text", "")
                position = mod.get("position", "bottom")
                prompt_parts.append(
                    f"{i}. Add text overlay '{overlay_text}' at {position}"
                )
            
            elif mod_type == "remove_element":
                element = mod.get("element", "")
                prompt_parts.append(
                    f"{i}. Remove {element} from the video"
                )
            
            elif mod_type == "change_colors":
                color_scheme = mod.get("colors", "")
                prompt_parts.append(
                    f"{i}. Adjust color scheme to {color_scheme}"
                )
            
            elif mod_type == "adjust_pacing":
                pacing = mod.get("pacing", "")
                prompt_parts.append(
                    f"{i}. Adjust video pacing to be more {pacing}"
                )
            
            else:
                # Generic modification
                instruction = mod.get("instruction", "")
                if instruction:
                    prompt_parts.append(f"{i}. {instruction}")
        
        return "\n".join(prompt_parts)
    
    def parse_modification_request(self, user_request: str) -> List[Dict[str, Any]]:
        """
        Parse natural language modification request into structured modifications
        
        Args:
            user_request: User's description of desired changes
            
        Returns:
            List of structured modification dictionaries
        """
        modifications = []
        request_lower = user_request.lower()
        
        # Check for text replacement
        if "change" in request_lower and "text" in request_lower:
            modifications.append({
                "type": "replace_text",
                "instruction": user_request,
            })
        
        # Check for pricing updates
        if any(word in request_lower for word in ["price", "pricing", "cost", "$"]):
            import re
            price_match = re.search(r'\$?\d+(?:,\d{3})*(?:\.\d{2})?', user_request)
            if price_match:
                modifications.append({
                    "type": "update_pricing",
                    "price": price_match.group(0),
                })
        
        # Check for vehicle changes
        if "vehicle" in request_lower or "car" in request_lower:
            modifications.append({
                "type": "change_vehicle",
                "instruction": user_request,
            })
        
        # Check for style changes
        style_keywords = ["professional", "dynamic", "friendly", "luxury", "casual"]
        for style in style_keywords:
            if style in request_lower:
                modifications.append({
                    "type": "change_style",
                    "style": style,
                })
                break
        
        # Check for seasonal themes
        if "winter" in request_lower or "summer" in request_lower:
            season = "winter" if "winter" in request_lower else "summer"
            modifications.append({
                "type": "change_style",
                "style": f"{season}-themed",
                "instruction": f"Update visuals for {season} theme",
            })
        
        # Check for color changes
        if "color" in request_lower or "colour" in request_lower:
            modifications.append({
                "type": "change_colors",
                "instruction": user_request,
            })
        
        # Check for overlay additions
        if "add" in request_lower and any(word in request_lower for word in ["text", "overlay", "label"]):
            modifications.append({
                "type": "add_overlay",
                "instruction": user_request,
            })
        
        # If no specific modifications detected, add as general instruction
        if not modifications:
            modifications.append({
                "type": "general",
                "instruction": user_request,
            })
        
        return modifications
    
    def suggest_improvements(
        self,
        video_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Suggest improvements based on video analysis
        
        Args:
            video_analysis: Analysis results from VideoAnalyzer
            
        Returns:
            List of suggested improvements
        """
        suggestions = []
        
        # Check video duration
        duration = video_analysis.get("duration", 0)
        if duration > 45:
            suggestions.append({
                "type": "duration",
                "suggestion": "Consider shortening to 30-45 seconds for better engagement",
                "priority": "medium",
            })
        
        # Check resolution
        resolution = video_analysis.get("resolution", "")
        if "720" in resolution:
            suggestions.append({
                "type": "quality",
                "suggestion": "Consider upgrading to 1080p for better quality",
                "priority": "low",
            })
        
        # Check text visibility
        detected_text = video_analysis.get("detected_text", [])
        if len(detected_text) > 5:
            suggestions.append({
                "type": "text",
                "suggestion": "Too much text - consider simplifying messaging",
                "priority": "high",
            })
        
        # Check style tags
        style_tags = video_analysis.get("style_tags", [])
        if "outdated" in style_tags or "old" in style_tags:
            suggestions.append({
                "type": "style",
                "suggestion": "Update visual style to more modern aesthetic",
                "priority": "high",
            })
        
        return suggestions
    
    def batch_customize(
        self,
        video_paths: List[str],
        common_modifications: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Apply same modifications to multiple videos
        
        Args:
            video_paths: List of video file paths
            common_modifications: Modifications to apply to all
            
        Returns:
            List of results for each video
        """
        results = []
        
        for video_path in video_paths:
            result = self.customize(
                source_video_path=video_path,
                modifications=common_modifications,
            )
            results.append({
                "source": video_path,
                "result": result,
            })
        
        return results
    
    def preview_modifications(
        self,
        modifications: List[Dict[str, Any]]
    ) -> str:
        """
        Generate a preview description of modifications
        
        Args:
            modifications: List of modifications
            
        Returns:
            Human-readable description
        """
        if not modifications:
            return "No modifications specified"
        
        descriptions = []
        for mod in modifications:
            mod_type = mod.get("type", "general")
            
            if mod_type == "replace_text":
                descriptions.append(
                    f"Replace '{mod.get('old_text')}' with '{mod.get('new_text')}'"
                )
            elif mod_type == "update_pricing":
                descriptions.append(f"Update pricing to {mod.get('price')}")
            elif mod_type == "change_vehicle":
                descriptions.append(f"Change vehicle to {mod.get('vehicle')}")
            elif mod_type == "change_style":
                descriptions.append(f"Adjust style to be {mod.get('style')}")
            else:
                descriptions.append(mod.get("instruction", "Apply modification"))
        
        return "Modifications to apply:\n- " + "\n- ".join(descriptions)
