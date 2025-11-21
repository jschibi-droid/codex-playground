"""
Video Template Definitions

Pre-configured templates for common dealership video scenarios.
"""

from dataclasses import dataclass
from typing import Literal, Optional


VideoType = Literal["sales", "service"]


@dataclass
class VideoTemplate:
    """Represents a video template"""
    
    id: str
    name: str
    type: VideoType
    duration: int
    style: str
    description: str
    scene_description: str
    focus_elements: str
    text_overlay_template: str
    suggested_cta: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "duration": self.duration,
            "style": self.style,
            "description": self.description,
            "scene_description": self.scene_description,
            "focus_elements": self.focus_elements,
            "text_overlay_template": self.text_overlay_template,
            "suggested_cta": self.suggested_cta,
        }


# Sales Templates
SALES_TEMPLATES = [
    VideoTemplate(
        id="new_inventory_showcase",
        name="New Inventory Showcase",
        type="sales",
        duration=30,
        style="dynamic",
        description="Showcase new vehicle arrivals with features and pricing",
        scene_description=(
            "Modern dealership showroom with multiple new vehicles on display. "
            "Bright, inviting atmosphere with spotlights highlighting vehicle features. "
            "Camera moves between vehicles showing different angles and details."
        ),
        focus_elements=(
            "- Exterior beauty shots (360° views)\n"
            "- Interior features and technology\n"
            "- Key specifications and highlights\n"
            "- Pricing and availability"
        ),
        text_overlay_template=(
            "Headline: 'NEW ARRIVALS'\n"
            "Vehicle: '{make} {model} {year}'\n"
            "Features: '{key_features}'\n"
            "Price: 'Starting at ${price}'\n"
            "CTA: '{call_to_action}'"
        ),
        suggested_cta="Visit us today for a test drive!",
    ),
    VideoTemplate(
        id="financing_promotion",
        name="Special Financing Offer",
        type="sales",
        duration=30,
        style="professional",
        description="Highlight special financing offers and incentives",
        scene_description=(
            "Professional showroom setting with featured vehicles. "
            "Clean, bright environment emphasizing value and opportunity. "
            "Focus on families, first-time buyers, or target demographic interacting with vehicles."
        ),
        focus_elements=(
            "- Featured vehicle(s) with financing offer\n"
            "- Visual representation of savings\n"
            "- Terms and conditions display\n"
            "- Happy customer scenarios"
        ),
        text_overlay_template=(
            "Headline: 'SPECIAL FINANCING OFFER'\n"
            "Offer: '{offer_details}'\n"
            "Terms: '{apr}% APR for {months} months'\n"
            "Eligible: '{eligible_models}'\n"
            "CTA: '{call_to_action}'"
        ),
        suggested_cta="Apply now! Limited time offer.",
    ),
    VideoTemplate(
        id="trade_in_promotion",
        name="Trade-In Event",
        type="sales",
        duration=30,
        style="friendly",
        description="Promote trade-in offers and upgrade opportunities",
        scene_description=(
            "Dealership exterior and showroom with customers bringing in trade vehicles. "
            "Welcoming atmosphere showing the ease of trading in. "
            "Display of upgrade options and new vehicles available."
        ),
        focus_elements=(
            "- Trade-in process simplicity\n"
            "- Value proposition and benefits\n"
            "- Upgrade vehicle showcase\n"
            "- Customer satisfaction moments"
        ),
        text_overlay_template=(
            "Headline: 'TOP DOLLAR FOR YOUR TRADE'\n"
            "Offer: '{trade_offer}'\n"
            "Bonus: '{additional_incentive}'\n"
            "Process: 'Quick & Easy Appraisal'\n"
            "CTA: '{call_to_action}'"
        ),
        suggested_cta="Get your free appraisal today!",
    ),
    VideoTemplate(
        id="seasonal_sale",
        name="Seasonal Sale Event",
        type="sales",
        duration=30,
        style="dynamic",
        description="Promote seasonal sales events and clearance",
        scene_description=(
            "Energetic showroom or outdoor lot with sale signage and featured inventory. "
            "Seasonal decorations or themes (summer, winter, holiday). "
            "Multiple vehicles with visible pricing/discount tags."
        ),
        focus_elements=(
            "- Sale event branding\n"
            "- Featured vehicles with savings\n"
            "- Limited-time urgency\n"
            "- Wide selection showcase"
        ),
        text_overlay_template=(
            "Headline: '{event_name}'\n"
            "Savings: 'Save up to ${max_savings}'\n"
            "Duration: '{start_date} - {end_date}'\n"
            "Details: '{sale_details}'\n"
            "CTA: '{call_to_action}'"
        ),
        suggested_cta="Hurry in - sale ends soon!",
    ),
    VideoTemplate(
        id="luxury_showcase",
        name="Luxury Vehicle Showcase",
        type="sales",
        duration=45,
        style="luxury",
        description="Premium presentation of luxury vehicles",
        scene_description=(
            "Elegant showroom or sophisticated outdoor setting with dramatic lighting. "
            "Close-up shots of premium materials, technology, and craftsmanship. "
            "Slow, deliberate camera movements emphasizing exclusivity."
        ),
        focus_elements=(
            "- Premium interior materials and finishes\n"
            "- Advanced technology features\n"
            "- Performance capabilities\n"
            "- Exclusive ownership benefits"
        ),
        text_overlay_template=(
            "Headline: '{vehicle_name}'\n"
            "Tagline: '{luxury_tagline}'\n"
            "Features: '{premium_features}'\n"
            "Experience: 'Schedule your exclusive preview'\n"
            "CTA: '{call_to_action}'"
        ),
        suggested_cta="Contact us for a private showing",
    ),
]


# Service Templates
SERVICE_TEMPLATES = [
    VideoTemplate(
        id="seasonal_maintenance",
        name="Seasonal Maintenance Package",
        type="service",
        duration=30,
        style="professional",
        description="Promote seasonal vehicle maintenance services",
        scene_description=(
            "Clean, modern service bay with technicians performing maintenance. "
            "Professional environment showing expertise and care. "
            "Focus on seasonal preparation (winter/summer) and vehicle protection."
        ),
        focus_elements=(
            "- Service bay operations\n"
            "- Technician expertise\n"
            "- Package contents and benefits\n"
            "- Vehicle protection benefits"
        ),
        text_overlay_template=(
            "Headline: '{season} VEHICLE PREP'\n"
            "Package: '{package_name}'\n"
            "Includes: '{services_included}'\n"
            "Price: '${package_price}'\n"
            "CTA: '{call_to_action}'"
        ),
        suggested_cta="Schedule your service today!",
    ),
    VideoTemplate(
        id="express_service",
        name="Express Service Convenience",
        type="service",
        duration=30,
        style="friendly",
        description="Highlight quick, convenient service options",
        scene_description=(
            "Fast-paced service center showing efficient operations. "
            "Customer waiting area with amenities. "
            "Quick turnaround emphasis with time-lapse elements."
        ),
        focus_elements=(
            "- Speed and efficiency\n"
            "- No appointment necessary\n"
            "- Comfortable waiting area\n"
            "- Common services offered"
        ),
        text_overlay_template=(
            "Headline: 'EXPRESS SERVICE'\n"
            "Services: '{service_list}'\n"
            "Time: '{typical_duration} minutes or less'\n"
            "Convenience: '{convenience_features}'\n"
            "CTA: '{call_to_action}'"
        ),
        suggested_cta="Drive in today - no appointment needed!",
    ),
    VideoTemplate(
        id="tire_service_special",
        name="Tire Service Special",
        type="service",
        duration=30,
        style="professional",
        description="Promote tire sales and services",
        scene_description=(
            "Service bay with tire displays and installation equipment. "
            "Technicians performing tire service professionally. "
            "Focus on tire quality, safety, and proper installation."
        ),
        focus_elements=(
            "- Tire selection and quality\n"
            "- Installation process\n"
            "- Safety benefits\n"
            "- Special pricing or packages"
        ),
        text_overlay_template=(
            "Headline: '{offer_title}'\n"
            "Package: '{package_details}'\n"
            "Includes: 'Installation, Balancing, Alignment'\n"
            "Price: '${package_price}'\n"
            "CTA: '{call_to_action}'"
        ),
        suggested_cta="Schedule your tire service now!",
    ),
    VideoTemplate(
        id="service_loyalty",
        name="Service Loyalty Program",
        type="service",
        duration=30,
        style="friendly",
        description="Promote service membership or loyalty programs",
        scene_description=(
            "Happy customers and service advisors interacting. "
            "Service center showing various maintenance activities. "
            "Visual representations of savings and benefits."
        ),
        focus_elements=(
            "- Program benefits showcase\n"
            "- Savings calculations\n"
            "- Member perks and advantages\n"
            "- Easy enrollment process"
        ),
        text_overlay_template=(
            "Headline: '{program_name}'\n"
            "Benefits: '{key_benefits}'\n"
            "Savings: 'Save up to ${annual_savings}/year'\n"
            "Members: '{member_perks}'\n"
            "CTA: '{call_to_action}'"
        ),
        suggested_cta="Join today and start saving!",
    ),
    VideoTemplate(
        id="certified_technicians",
        name="Certified Technician Expertise",
        type="service",
        duration=30,
        style="professional",
        description="Highlight technician expertise and certifications",
        scene_description=(
            "Professional service center with certified technicians at work. "
            "Display of certifications, training, and advanced equipment. "
            "Customer trust and satisfaction emphasis."
        ),
        focus_elements=(
            "- Technician credentials\n"
            "- Advanced diagnostic equipment\n"
            "- Quality workmanship\n"
            "- Customer satisfaction"
        ),
        text_overlay_template=(
            "Headline: 'CERTIFIED EXPERTISE'\n"
            "Credentials: '{certifications}'\n"
            "Experience: '{experience_details}'\n"
            "Quality: 'Guaranteed Workmanship'\n"
            "CTA: '{call_to_action}'"
        ),
        suggested_cta="Trust the experts - schedule today!",
    ),
]


def get_template_by_id(template_id: str) -> Optional[VideoTemplate]:
    """Get a template by its ID"""
    all_templates = SALES_TEMPLATES + SERVICE_TEMPLATES
    for template in all_templates:
        if template.id == template_id:
            return template
    return None


def get_templates_by_type(video_type: VideoType) -> list[VideoTemplate]:
    """Get all templates of a specific type"""
    if video_type == "sales":
        return SALES_TEMPLATES
    elif video_type == "service":
        return SERVICE_TEMPLATES
    return []


def list_all_templates() -> list[VideoTemplate]:
    """Get all available templates"""
    return SALES_TEMPLATES + SERVICE_TEMPLATES
