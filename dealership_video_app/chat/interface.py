"""
Main Chat Interface

Primary interface for interacting with the dealership video generation system.
"""

from typing import Optional, Dict, Any
import uuid
from .context_manager import ConversationContext
from .conversation_flow import ConversationFlow
from .intent_classifier import IntentClassifier


class DealershipChatInterface:
    """
    Main chat interface for video creation workflow
    
    This class manages the conversation with users, guiding them through
    the video creation process using Gemini 3.0 for natural language interaction.
    """
    
    def __init__(self, gemini_client: Optional[Any] = None):
        """
        Initialize chat interface
        
        Args:
            gemini_client: Optional Gemini API client for AI-powered responses
        """
        self.gemini_client = gemini_client
        self.context = ConversationContext(session_id=str(uuid.uuid4()))
        self.flow = ConversationFlow()
        self.intent_classifier = IntentClassifier()
    
    def start_conversation(self) -> str:
        """
        Start a new conversation
        
        Returns:
            Initial greeting and question
        """
        self.context.stage = "initial"
        initial_message = self.flow.get_initial_question()
        self.context.add_message("assistant", initial_message)
        return initial_message
    
    def process_message(self, user_input: str) -> str:
        """
        Process user message and generate response
        
        Args:
            user_input: User's message
            
        Returns:
            Assistant's response
        """
        # Add user message to history
        self.context.add_message("user", user_input)
        
        # Parse user input and update context
        self.context = self.flow.parse_user_response(user_input, self.context)
        
        # Update conversation stage
        self._update_stage()
        
        # Generate response
        response = self._generate_response(user_input)
        
        # Add assistant response to history
        self.context.add_message("assistant", response)
        
        return response
    
    def _update_stage(self) -> None:
        """Update conversation stage based on context"""
        if not self.context.video_intent:
            self.context.stage = "intent_gathering"
        elif not self.context.workflow_type:
            self.context.stage = "workflow_selection"
        elif self.context.workflow_type == "upload_based" and not self.context.uploaded_video_path:
            self.context.stage = "video_upload"
        elif not self.context.is_ready_for_generation():
            self.context.stage = "details_gathering"
        else:
            self.context.stage = "ready_for_generation"
    
    def _generate_response(self, user_input: str) -> str:
        """
        Generate appropriate response based on context
        
        Args:
            user_input: User's latest input
            
        Returns:
            Generated response
        """
        # If using Gemini, generate AI response
        if self.gemini_client:
            return self._generate_ai_response(user_input)
        
        # Otherwise, use rule-based response
        return self._generate_rule_based_response(user_input)
    
    def _generate_rule_based_response(self, user_input: str) -> str:
        """Generate response using rule-based logic"""
        user_lower = user_input.lower()
        
        # Handle confirmation/ready for generation
        if self.context.stage == "ready_for_generation":
            if any(word in user_lower for word in ["yes", "sure", "okay", "go ahead", "generate"]):
                return (
                    "Great! I'm generating your video now. This may take a few moments...\n\n"
                    "I'll create a professional video based on all the details you've provided."
                )
            elif any(word in user_lower for word in ["no", "wait", "change"]):
                return "No problem! What would you like to change?"
        
        # Check if ready for generation
        if self.context.is_ready_for_generation() and self.context.stage == "details_gathering":
            self.context.stage = "ready_for_generation"
            return self.flow.generate_confirmation_message(self.context)
        
        # Get next question
        next_question = self.flow.get_next_question(self.context)
        
        if next_question:
            return next_question
        
        # Fallback: ask if ready to generate
        missing = self.context.get_missing_information()
        if missing:
            return (
                f"I still need a bit more information:\n"
                f"- {', '.join(missing)}\n\n"
                f"Could you provide these details?"
            )
        
        return "I have all the information I need. Ready to generate your video?"
    
    def _generate_ai_response(self, user_input: str) -> str:
        """
        Generate AI-powered response using Gemini
        
        Args:
            user_input: User's latest input
            
        Returns:
            AI-generated response
        """
        # This would integrate with Gemini API
        # For now, fall back to rule-based
        return self._generate_rule_based_response(user_input)
    
    def get_context(self) -> ConversationContext:
        """Get current conversation context"""
        return self.context
    
    def get_context_summary(self) -> str:
        """Get human-readable context summary"""
        return self.context.get_conversation_summary()
    
    def is_ready_for_generation(self) -> bool:
        """Check if ready to generate video"""
        return self.context.is_ready_for_generation()
    
    def get_video_prompt(self) -> Optional[str]:
        """
        Get the generated video prompt for Veo
        
        Returns:
            Generated prompt or None if not ready
        """
        if not self.is_ready_for_generation():
            return None
        
        return self._build_video_prompt()
    
    def _build_video_prompt(self) -> str:
        """Build detailed video generation prompt"""
        from ..config.veo_config import build_veo_prompt
        
        context = self.context
        
        # Determine video type
        video_type = f"{context.video_intent}_advertising" if context.video_intent else "dealership_video"
        
        # Build scene description
        if context.video_intent == "sales":
            scene_description = self._build_sales_scene()
        elif context.video_intent == "service":
            scene_description = self._build_service_scene()
        else:
            scene_description = "Professional car dealership environment"
        
        # Build focus elements
        focus_elements = self._build_focus_elements()
        
        # Build text overlays
        text_overlays = self._build_text_overlays()
        
        # Build environment
        environment = "Modern car dealership showroom" if context.video_intent == "sales" else "Professional service center"
        
        # Build prompt
        prompt = build_veo_prompt(
            video_type=video_type,
            duration=context.duration,
            style=context.tone or "professional",  # type: ignore
            quality=context.quality,  # type: ignore
            scene_description=scene_description,
            focus_elements=focus_elements,
            text_overlays=text_overlays,
            environment=environment,
        )
        
        self.context.generated_prompt = prompt
        return prompt
    
    def _build_sales_scene(self) -> str:
        """Build scene description for sales video"""
        parts = ["Modern car dealership showroom with professional lighting."]
        
        if self.context.vehicle_make or self.context.vehicle_model:
            vehicle = f"{self.context.vehicle_year or ''} {self.context.vehicle_make or ''} {self.context.vehicle_model or ''}".strip()
            parts.append(f"Featured vehicle: {vehicle}.")
        
        if self.context.target_audience:
            parts.append(f"Appealing to {self.context.target_audience}.")
        
        if self.context.special_offers:
            parts.append("Highlighting special promotional offer.")
        
        return " ".join(parts)
    
    def _build_service_scene(self) -> str:
        """Build scene description for service video"""
        parts = ["Professional automotive service center with clean, organized environment."]
        
        if self.context.service_type:
            parts.append(f"Showcasing {self.context.service_type} service.")
        
        if self.context.seasonal_focus:
            parts.append(f"Emphasizing {self.context.seasonal_focus} seasonal preparation.")
        
        parts.append("Certified technicians performing quality work.")
        
        return " ".join(parts)
    
    def _build_focus_elements(self) -> str:
        """Build focus elements description"""
        elements = []
        
        if self.context.video_intent == "sales":
            if self.context.vehicle_make or self.context.vehicle_model:
                elements.append("- Exterior and interior vehicle features")
                elements.append("- Key technology and specifications")
            if self.context.special_offers:
                elements.append("- Promotional offer details")
            elements.append("- Dealership branding and contact information")
        
        elif self.context.video_intent == "service":
            if self.context.service_type:
                elements.append(f"- {self.context.service_type} process and benefits")
            elements.append("- Technician expertise and certifications")
            elements.append("- Customer satisfaction and trust")
            if self.context.package_price:
                elements.append(f"- Package pricing: {self.context.package_price}")
        
        return "\n".join(elements) if elements else "- Professional dealership presentation"
    
    def _build_text_overlays(self) -> str:
        """Build text overlays description"""
        overlays = []
        
        # Headline
        if self.context.main_message:
            overlays.append(f"Headline: {self.context.main_message[:50]}")
        elif self.context.video_intent == "sales":
            vehicle = f"{self.context.vehicle_year or ''} {self.context.vehicle_make or ''} {self.context.vehicle_model or ''}".strip()
            if vehicle:
                overlays.append(f"Headline: {vehicle}")
        elif self.context.video_intent == "service":
            if self.context.service_type:
                overlays.append(f"Headline: {self.context.service_type.title()}")
        
        # Details
        if self.context.special_offers:
            overlays.append(f"Offer: {self.context.special_offers}")
        if self.context.package_price:
            overlays.append(f"Price: {self.context.package_price}")
        
        # Call-to-action
        if self.context.call_to_action:
            overlays.append(f"CTA: {self.context.call_to_action}")
        
        return "\n".join(overlays) if overlays else "Standard dealership information"
    
    def reset_conversation(self) -> str:
        """Reset conversation and start fresh"""
        self.context = ConversationContext(session_id=str(uuid.uuid4()))
        return self.start_conversation()
