"""
Conversation Flow Management

Manages the dialog flow and guides users through the video creation process.
"""

import re
from typing import Optional, List
from .context_manager import ConversationContext
from .intent_classifier import IntentClassifier, VideoIntent
from ..config.templates import get_templates_by_type, list_all_templates


class ConversationFlow:
    """Manages conversation flow and generates appropriate questions"""
    
    def __init__(self):
        self.intent_classifier = IntentClassifier()
    
    def get_initial_question(self) -> str:
        """Get the initial question to start the conversation"""
        return (
            "Hello! I'm here to help you create a professional video for your dealership. "
            "Are you creating content for **sales** advertising (showcasing vehicles, promotions) "
            "or **service** advertising (maintenance, repairs, service packages)?"
        )
    
    def get_workflow_question(self) -> str:
        """Ask about workflow preference"""
        return (
            "Great! Would you like to:\n"
            "1. **Describe** what you want and I'll generate a video from scratch\n"
            "2. **Upload** an existing video and customize it\n\n"
            "Which option would you prefer?"
        )
    
    def get_next_question(self, context: ConversationContext) -> Optional[str]:
        """
        Determine the next question based on conversation context
        
        Args:
            context: Current conversation context
            
        Returns:
            Next question to ask, or None if ready for generation
        """
        # If intent not determined, ask for it
        if not context.video_intent:
            return self.get_initial_question()
        
        # If workflow not determined, ask for it
        if not context.workflow_type:
            return self.get_workflow_question()
        
        # For upload workflow, guide through video upload
        if context.workflow_type == "upload_based" and not context.uploaded_video_path:
            return "Please upload your video file, and I'll analyze it for you."
        
        # Get missing information based on intent
        if context.video_intent == "sales":
            return self._get_sales_questions(context)
        elif context.video_intent == "service":
            return self._get_service_questions(context)
        
        return None
    
    def _get_sales_questions(self, context: ConversationContext) -> Optional[str]:
        """Get next question for sales video creation"""
        
        # Offer template selection
        if not context.template_id and not context.main_message:
            templates = get_templates_by_type("sales")
            template_list = "\n".join([
                f"- **{t.name}**: {t.description}" for t in templates
            ])
            return (
                f"Would you like to use one of our sales video templates?\n\n{template_list}\n\n"
                "Or you can describe your own custom video. What would you prefer?"
            )
        
        # Ask about vehicle details
        if not context.vehicle_make and not context.vehicle_model:
            return "What vehicle(s) would you like to feature? (e.g., 2024 Honda CR-V)"
        
        # Ask about special offers
        if not context.special_offers and not context.pricing:
            return "Do you have any special offers, financing deals, or pricing you'd like to highlight?"
        
        # Ask about target audience
        if not context.target_audience:
            return (
                "Who is your target audience? "
                "(e.g., families, first-time buyers, luxury shoppers, young professionals)"
            )
        
        # Ask about tone
        if not context.tone:
            return (
                "What tone would you like for the video?\n"
                "- **Professional**: Clean, corporate, polished\n"
                "- **Dynamic**: Exciting, fast-paced, energetic\n"
                "- **Friendly**: Warm, family-oriented, approachable\n"
                "- **Luxury**: Premium, sophisticated, elegant"
            )
        
        # Ask about call-to-action
        if not context.call_to_action:
            return (
                "What call-to-action would you like? "
                "(e.g., 'Schedule a test drive', 'Visit us today', 'Apply for financing')"
            )
        
        # Ready for generation
        return None
    
    def _get_service_questions(self, context: ConversationContext) -> Optional[str]:
        """Get next question for service video creation"""
        
        # Offer template selection
        if not context.template_id and not context.main_message:
            templates = get_templates_by_type("service")
            template_list = "\n".join([
                f"- **{t.name}**: {t.description}" for t in templates
            ])
            return (
                f"Would you like to use one of our service video templates?\n\n{template_list}\n\n"
                "Or you can describe your own custom video. What would you prefer?"
            )
        
        # Ask about service type
        if not context.service_type and not context.service_package:
            return (
                "What type of service would you like to promote? "
                "(e.g., oil change, tire service, seasonal maintenance, brake service)"
            )
        
        # Ask about seasonal focus
        if not context.seasonal_focus and "seasonal" in (context.service_type or "").lower():
            return "Is this for winter preparation or summer maintenance?"
        
        # Ask about package details
        if not context.package_price and context.service_package:
            return f"What's the price for the {context.service_package}?"
        
        # Ask about tone
        if not context.tone:
            return (
                "What tone would you like for the video?\n"
                "- **Professional**: Trustworthy, expert, polished\n"
                "- **Friendly**: Approachable, helpful, welcoming\n"
                "- **Efficient**: Quick, convenient, no-nonsense"
            )
        
        # Ask about call-to-action
        if not context.call_to_action:
            return (
                "What call-to-action would you like? "
                "(e.g., 'Schedule service today', 'Book online', 'Drive in - no appointment needed')"
            )
        
        # Ready for generation
        return None
    
    def suggest_template(self, context: ConversationContext) -> Optional[str]:
        """
        Suggest an appropriate template based on context
        
        Returns:
            Template ID or None
        """
        if not context.video_intent:
            return None
        
        templates = get_templates_by_type(context.video_intent)  # type: ignore
        
        if not templates:
            return None
        
        # Try to match based on keywords in the context
        if context.video_intent == "sales":
            if context.special_offers and "financing" in context.special_offers.lower():
                return "financing_promotion"
            elif context.special_offers and "trade" in context.special_offers.lower():
                return "trade_in_promotion"
            elif context.tone == "luxury":
                return "luxury_showcase"
            else:
                return "new_inventory_showcase"
        
        elif context.video_intent == "service":
            if context.service_type:
                service_lower = context.service_type.lower()
                if "tire" in service_lower:
                    return "tire_service_special"
                elif "seasonal" in service_lower or context.seasonal_focus:
                    return "seasonal_maintenance"
                elif "express" in service_lower or "quick" in service_lower:
                    return "express_service"
            return "seasonal_maintenance"
        
        return None
    
    def generate_confirmation_message(self, context: ConversationContext) -> str:
        """Generate a confirmation message before video generation"""
        summary_parts = [
            "Perfect! Here's what I have:",
            "",
            f"**Video Type**: {context.video_intent.title() if context.video_intent else 'Unknown'}",
        ]
        
        if context.video_intent == "sales":
            if context.vehicle_make or context.vehicle_model:
                vehicle = f"{context.vehicle_year or ''} {context.vehicle_make or ''} {context.vehicle_model or ''}".strip()
                summary_parts.append(f"**Vehicle**: {vehicle}")
            if context.special_offers:
                summary_parts.append(f"**Offer**: {context.special_offers}")
        
        elif context.video_intent == "service":
            if context.service_type:
                summary_parts.append(f"**Service**: {context.service_type}")
            if context.service_package:
                summary_parts.append(f"**Package**: {context.service_package}")
            if context.package_price:
                summary_parts.append(f"**Price**: {context.package_price}")
        
        if context.target_audience:
            summary_parts.append(f"**Audience**: {context.target_audience}")
        
        if context.tone:
            summary_parts.append(f"**Tone**: {context.tone}")
        
        if context.call_to_action:
            summary_parts.append(f"**Call-to-Action**: {context.call_to_action}")
        
        summary_parts.extend([
            f"**Duration**: {context.duration} seconds",
            "",
            "Shall I generate the video with these details?"
        ])
        
        return "\n".join(summary_parts)
    
    def parse_user_response(
        self, 
        user_input: str, 
        context: ConversationContext
    ) -> ConversationContext:
        """
        Parse user input and update context
        
        Args:
            user_input: User's message
            context: Current conversation context
            
        Returns:
            Updated context
        """
        user_input_lower = user_input.lower()
        
        # Detect intent if not set
        if not context.video_intent:
            intent = self.intent_classifier.classify(user_input)
            if intent != VideoIntent.UNKNOWN:
                context.video_intent = intent.value
        
        # Detect workflow type
        if not context.workflow_type:
            if any(word in user_input_lower for word in ["upload", "existing", "customize", "modify"]):
                context.workflow_type = "upload_based"
            elif any(word in user_input_lower for word in ["describe", "scratch", "new", "create"]):
                context.workflow_type = "prompt_based"
        
        # Extract vehicle information for sales
        if context.video_intent == "sales":
            vehicle_info = self.intent_classifier.extract_vehicle_info(user_input)
            if vehicle_info["year"]:
                context.vehicle_year = vehicle_info["year"]
            if vehicle_info["make"]:
                context.vehicle_make = vehicle_info["make"]
            if vehicle_info["model"]:
                context.vehicle_model = vehicle_info["model"]
            
            # Check for pricing/offers
            if any(word in user_input_lower for word in ["financing", "apr", "lease", "price", "offer", "special"]):
                if not context.special_offers:
                    context.special_offers = user_input
        
        # Extract service information
        if context.video_intent == "service":
            service_info = self.intent_classifier.extract_service_info(user_input)
            if service_info["service_type"]:
                context.service_type = service_info["service_type"]
            if service_info["seasonal"]:
                context.seasonal_focus = service_info["seasonal"]
            
            # Check for package/pricing mentions
            if "package" in user_input_lower and not context.service_package:
                context.service_package = user_input
            
            # Extract price
            price_match = re.search(r'\$?\d+(?:,\d{3})*(?:\.\d{2})?', user_input)
            if price_match and not context.package_price:
                context.package_price = price_match.group(0)
        
        # Extract tone
        tone = self.intent_classifier.extract_tone(user_input)
        if tone and not context.tone:
            context.tone = tone
        
        # Extract duration
        duration = self.intent_classifier.extract_duration(user_input)
        if duration:
            context.duration = min(duration, 60)  # Cap at 60 seconds
        
        # Check for call-to-action phrases
        cta_phrases = [
            "visit", "schedule", "call", "contact", "book", "apply",
            "drive in", "come in", "stop by", "test drive"
        ]
        if any(phrase in user_input_lower for phrase in cta_phrases) and not context.call_to_action:
            context.call_to_action = user_input
        
        # Capture main message if substantial
        if len(user_input) > 20 and not context.main_message:
            context.main_message = user_input
        
        return context
