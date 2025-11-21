"""
Conversation Context Manager

Maintains conversation state and context throughout the video creation session.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ConversationContext:
    """Manages conversation state and collected information"""
    
    # Conversation metadata
    session_id: str = ""
    stage: str = "initial"  # initial, intent_gathering, details, generation, customization
    
    # Intent and type
    video_intent: Optional[str] = None  # "sales" or "service"
    workflow_type: Optional[str] = None  # "prompt_based" or "upload_based"
    
    # Video specifications
    video_type: Optional[str] = None
    duration: int = 30
    style: str = "professional"
    quality: str = "high"
    
    # Content details
    target_audience: Optional[str] = None
    main_message: Optional[str] = None
    tone: Optional[str] = None
    call_to_action: Optional[str] = None
    
    # Sales-specific
    vehicle_make: Optional[str] = None
    vehicle_model: Optional[str] = None
    vehicle_year: Optional[int] = None
    pricing: Optional[str] = None
    special_offers: Optional[str] = None
    inventory_details: Optional[str] = None
    
    # Service-specific
    service_type: Optional[str] = None
    service_package: Optional[str] = None
    package_price: Optional[str] = None
    seasonal_focus: Optional[str] = None
    
    # Template
    template_id: Optional[str] = None
    template_customizations: Dict[str, Any] = field(default_factory=dict)
    
    # Video customization (for upload workflow)
    uploaded_video_path: Optional[str] = None
    requested_modifications: List[str] = field(default_factory=list)
    
    # Generated content
    generated_prompt: Optional[str] = None
    video_url: Optional[str] = None
    
    # Conversation history
    messages: List[Dict[str, str]] = field(default_factory=list)
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history"""
        self.messages.append({"role": role, "content": content})
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation context"""
        summary_parts = []
        
        if self.video_intent:
            summary_parts.append(f"Intent: {self.video_intent}")
        
        if self.workflow_type:
            summary_parts.append(f"Workflow: {self.workflow_type}")
        
        if self.main_message:
            summary_parts.append(f"Message: {self.main_message}")
        
        if self.video_intent == "sales":
            if self.vehicle_make or self.vehicle_model:
                vehicle = f"{self.vehicle_year or ''} {self.vehicle_make or ''} {self.vehicle_model or ''}".strip()
                if vehicle:
                    summary_parts.append(f"Vehicle: {vehicle}")
            if self.special_offers:
                summary_parts.append(f"Offer: {self.special_offers}")
        
        elif self.video_intent == "service":
            if self.service_type:
                summary_parts.append(f"Service: {self.service_type}")
            if self.service_package:
                summary_parts.append(f"Package: {self.service_package}")
        
        if self.tone:
            summary_parts.append(f"Tone: {self.tone}")
        
        if self.template_id:
            summary_parts.append(f"Template: {self.template_id}")
        
        return " | ".join(summary_parts) if summary_parts else "New conversation"
    
    def is_ready_for_generation(self) -> bool:
        """Check if enough information has been gathered for video generation"""
        if not self.video_intent:
            return False
        
        # Must have main message or template
        if not self.main_message and not self.template_id:
            return False
        
        # For sales videos
        if self.video_intent == "sales":
            # Either have specific vehicle info or general sales message
            has_vehicle = bool(self.vehicle_make or self.vehicle_model)
            has_offer = bool(self.special_offers)
            if not (has_vehicle or has_offer or self.template_id):
                return False
        
        # For service videos
        elif self.video_intent == "service":
            # Must have service type or package
            if not (self.service_type or self.service_package or self.template_id):
                return False
        
        return True
    
    def get_missing_information(self) -> List[str]:
        """Get list of missing key information"""
        missing = []
        
        if not self.video_intent:
            missing.append("video intent (sales or service)")
        
        if not self.main_message and not self.template_id:
            missing.append("main message or template selection")
        
        if self.video_intent == "sales":
            if not (self.vehicle_make or self.vehicle_model or self.special_offers or self.template_id):
                missing.append("vehicle details or special offers")
        
        elif self.video_intent == "service":
            if not (self.service_type or self.service_package or self.template_id):
                missing.append("service type or package")
        
        if not self.tone:
            missing.append("desired tone")
        
        if not self.call_to_action:
            missing.append("call-to-action")
        
        return missing
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary"""
        return {
            "session_id": self.session_id,
            "stage": self.stage,
            "video_intent": self.video_intent,
            "workflow_type": self.workflow_type,
            "video_type": self.video_type,
            "duration": self.duration,
            "style": self.style,
            "quality": self.quality,
            "target_audience": self.target_audience,
            "main_message": self.main_message,
            "tone": self.tone,
            "call_to_action": self.call_to_action,
            "vehicle_make": self.vehicle_make,
            "vehicle_model": self.vehicle_model,
            "vehicle_year": self.vehicle_year,
            "pricing": self.pricing,
            "special_offers": self.special_offers,
            "service_type": self.service_type,
            "service_package": self.service_package,
            "template_id": self.template_id,
            "generated_prompt": self.generated_prompt,
            "video_url": self.video_url,
        }
