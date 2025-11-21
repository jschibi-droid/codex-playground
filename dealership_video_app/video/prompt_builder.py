"""
Video Prompt Builder

Constructs detailed prompts for Veo video generation.
"""

from typing import Dict, Any, Optional
from ..config.veo_config import build_veo_prompt, STYLE_PRESETS
from ..config.templates import VideoTemplate


class PromptBuilder:
    """
    Builds structured prompts for video generation
    
    Takes conversation context and constructs detailed Veo prompts
    optimized for car dealership video content.
    """
    
    def __init__(self):
        self.style_presets = STYLE_PRESETS
    
    def build_from_context(self, context: Any) -> str:
        """
        Build video prompt from conversation context
        
        Args:
            context: ConversationContext object
            
        Returns:
            Formatted video generation prompt
        """
        # Determine video type
        video_type = f"{context.video_intent}_advertising" if context.video_intent else "dealership_video"
        
        # Build components
        scene_description = self._build_scene_description(context)
        focus_elements = self._build_focus_elements(context)
        text_overlays = self._build_text_overlays(context)
        brand_elements = self._build_brand_elements(context)
        environment = self._determine_environment(context)
        audio_direction = self._build_audio_direction(context)
        
        # Use Veo config builder
        prompt = build_veo_prompt(
            video_type=video_type,
            duration=context.duration,
            style=context.tone or "professional",
            quality=context.quality,
            scene_description=scene_description,
            focus_elements=focus_elements,
            text_overlays=text_overlays,
            brand_elements=brand_elements,
            environment=environment,
            audio_direction=audio_direction,
        )
        
        return prompt
    
    def build_from_template(
        self,
        template: VideoTemplate,
        customizations: Dict[str, Any]
    ) -> str:
        """
        Build video prompt from template with customizations
        
        Args:
            template: VideoTemplate object
            customizations: Dictionary of custom values
            
        Returns:
            Formatted video generation prompt
        """
        # Apply customizations to template
        scene_description = template.scene_description
        focus_elements = template.focus_elements
        text_overlays = self._apply_template_customizations(
            template.text_overlay_template,
            customizations
        )
        
        prompt = build_veo_prompt(
            video_type=template.type,
            duration=template.duration,
            style=template.style,
            quality=customizations.get("quality", "high"),
            scene_description=scene_description,
            focus_elements=focus_elements,
            text_overlays=text_overlays,
        )
        
        return prompt
    
    def _build_scene_description(self, context: Any) -> str:
        """Build detailed scene description"""
        parts = []
        
        if context.video_intent == "sales":
            parts.append("Modern car dealership showroom with professional lighting and polished floors.")
            
            if context.vehicle_make or context.vehicle_model:
                vehicle = self._format_vehicle(context)
                parts.append(f"Featured vehicle: {vehicle}, prominently displayed.")
            
            if context.target_audience:
                audience_scenes = {
                    "families": "Family-friendly environment with spacious layout",
                    "luxury": "Sophisticated showroom with premium finishes",
                    "young professionals": "Contemporary, stylish showroom design",
                    "first-time buyers": "Welcoming, approachable atmosphere",
                }
                for key, scene in audience_scenes.items():
                    if key in context.target_audience.lower():
                        parts.append(scene + ".")
                        break
            
            if context.special_offers:
                parts.append("Eye-catching promotional signage visible.")
        
        elif context.video_intent == "service":
            parts.append("Professional automotive service center with clean, organized bays.")
            parts.append("State-of-the-art equipment and tools visible.")
            
            if context.service_type:
                service_scenes = {
                    "oil change": "Quick service bay with lift and oil collection systems",
                    "tire": "Tire display wall and installation equipment",
                    "brake": "Detailed brake service area with precision tools",
                    "diagnostic": "Advanced diagnostic computer systems",
                    "seasonal": "Comprehensive maintenance inspection area",
                }
                for key, scene in service_scenes.items():
                    if key in context.service_type.lower():
                        parts.append(scene + ".")
                        break
            
            parts.append("Certified technicians in clean uniforms working professionally.")
        
        return " ".join(parts)
    
    def _build_focus_elements(self, context: Any) -> str:
        """Build list of focus elements"""
        elements = []
        
        if context.video_intent == "sales":
            elements.append("- Exterior vehicle beauty shots (multiple angles)")
            elements.append("- Interior features and technology closeups")
            
            if context.vehicle_make or context.vehicle_model:
                elements.append("- Vehicle badge and branding details")
            
            if context.special_offers:
                elements.append("- Special offer details and terms")
            
            elements.append("- Dealership branding and contact information")
            
            if context.target_audience:
                if "family" in context.target_audience.lower():
                    elements.append("- Family-friendly features (space, safety)")
                elif "luxury" in context.target_audience.lower():
                    elements.append("- Premium materials and craftsmanship")
        
        elif context.video_intent == "service":
            if context.service_type:
                elements.append(f"- {context.service_type.title()} process demonstration")
            
            elements.append("- Technician expertise and certifications")
            elements.append("- Quality parts and materials")
            elements.append("- Clean, professional facility")
            
            if context.package_price:
                elements.append(f"- Package pricing: {context.package_price}")
            
            elements.append("- Customer satisfaction emphasis")
        
        return "\n".join(elements)
    
    def _build_text_overlays(self, context: Any) -> str:
        """Build text overlay specifications"""
        overlays = []
        
        # Main headline
        if context.main_message:
            headline = context.main_message[:50]
        elif context.video_intent == "sales":
            vehicle = self._format_vehicle(context)
            headline = vehicle if vehicle else "NEW ARRIVALS"
        elif context.video_intent == "service":
            service = context.service_type.title() if context.service_type else "QUALITY SERVICE"
            headline = service
        else:
            headline = "VISIT US TODAY"
        
        overlays.append(f"Headline: {headline}")
        
        # Details/offer
        if context.special_offers:
            overlays.append(f"Offer: {context.special_offers}")
        elif context.service_package:
            overlays.append(f"Package: {context.service_package}")
        
        # Pricing
        if context.pricing:
            overlays.append(f"Price: {context.pricing}")
        elif context.package_price:
            overlays.append(f"Price: {context.package_price}")
        
        # Call-to-action
        if context.call_to_action:
            overlays.append(f"CTA: {context.call_to_action}")
        else:
            default_cta = "Visit us today!" if context.video_intent == "sales" else "Schedule service now!"
            overlays.append(f"CTA: {default_cta}")
        
        return "\n".join(overlays)
    
    def _build_brand_elements(self, context: Any) -> str:
        """Build brand element specifications"""
        return (
            "Dealership logo prominently displayed. "
            "Brand colors consistent throughout. "
            "Contact information clearly visible at end."
        )
    
    def _determine_environment(self, context: Any) -> str:
        """Determine video environment"""
        if context.video_intent == "sales":
            return "Modern car dealership showroom with professional lighting"
        elif context.video_intent == "service":
            return "Professional automotive service center"
        return "Car dealership facility"
    
    def _build_audio_direction(self, context: Any) -> str:
        """Build audio/music direction"""
        if context.tone == "dynamic":
            return "Upbeat, energetic background music with professional voiceover"
        elif context.tone == "luxury":
            return "Sophisticated instrumental music with refined voiceover"
        elif context.tone == "friendly":
            return "Warm, inviting background music with conversational voiceover"
        else:
            return "Professional background music with clear, confident voiceover"
    
    def _format_vehicle(self, context: Any) -> str:
        """Format vehicle information as string"""
        parts = []
        if context.vehicle_year:
            parts.append(str(context.vehicle_year))
        if context.vehicle_make:
            parts.append(context.vehicle_make)
        if context.vehicle_model:
            parts.append(context.vehicle_model)
        return " ".join(parts)
    
    def _apply_template_customizations(
        self,
        template_text: str,
        customizations: Dict[str, Any]
    ) -> str:
        """Apply customizations to template text"""
        result = template_text
        for key, value in customizations.items():
            placeholder = "{" + key + "}"
            if placeholder in result:
                result = result.replace(placeholder, str(value))
        return result
    
    def enhance_prompt(self, base_prompt: str, enhancements: Dict[str, Any]) -> str:
        """
        Enhance an existing prompt with additional details
        
        Args:
            base_prompt: Base prompt text
            enhancements: Dictionary of enhancements to add
            
        Returns:
            Enhanced prompt
        """
        enhanced = base_prompt
        
        if enhancements.get("add_transitions"):
            enhanced += "\n\nTRANSITIONS:\nSmooth, professional transitions between scenes."
        
        if enhancements.get("add_effects"):
            effects = enhancements.get("effects", [])
            if effects:
                enhanced += f"\n\nVISUAL EFFECTS:\n{', '.join(effects)}"
        
        if enhancements.get("emphasize"):
            emphasis = enhancements.get("emphasize")
            enhanced += f"\n\nEMPHASIS:\nSpecial attention to: {emphasis}"
        
        return enhanced
