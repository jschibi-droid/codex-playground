"""
Intent Classification Module

Determines user intent from conversation (sales vs. service focus).
"""

from enum import Enum
from typing import Optional
import re


class VideoIntent(Enum):
    """Video intent types"""
    SALES = "sales"
    SERVICE = "service"
    UNKNOWN = "unknown"


class IntentClassifier:
    """Classifies user intent from conversation text"""
    
    # Keywords for sales intent
    SALES_KEYWORDS = {
        "inventory", "vehicle", "car", "truck", "suv", "sedan", "new arrivals",
        "test drive", "purchase", "buy", "financing", "lease", "trade-in",
        "sale", "special offer", "discount", "promotion", "price", "pricing",
        "deal", "model", "make", "stock", "available", "showroom"
    }
    
    # Keywords for service intent
    SERVICE_KEYWORDS = {
        "service", "maintenance", "repair", "oil change", "tire", "brake",
        "inspection", "diagnostic", "tune-up", "warranty", "technician",
        "appointment", "schedule", "service center", "parts", "filter",
        "rotation", "alignment", "battery", "fluid", "seasonal prep",
        "winter", "summer", "check-up"
    }
    
    def __init__(self):
        """Initialize the intent classifier"""
        pass
    
    def classify(self, text: str) -> VideoIntent:
        """
        Classify intent from text
        
        Args:
            text: User input text
            
        Returns:
            VideoIntent enum value
        """
        if not text:
            return VideoIntent.UNKNOWN
        
        text_lower = text.lower()
        
        # Count keyword matches
        sales_score = sum(1 for keyword in self.SALES_KEYWORDS if keyword in text_lower)
        service_score = sum(1 for keyword in self.SERVICE_KEYWORDS if keyword in text_lower)
        
        # Check for explicit mentions
        if re.search(r'\bsales?\b|\bselling\b', text_lower):
            sales_score += 2
        if re.search(r'\bservice\b|\bservicing\b', text_lower):
            service_score += 2
        
        # Determine intent based on scores
        if sales_score > service_score:
            return VideoIntent.SALES
        elif service_score > sales_score:
            return VideoIntent.SERVICE
        else:
            return VideoIntent.UNKNOWN
    
    def is_sales_intent(self, text: str) -> bool:
        """Check if text indicates sales intent"""
        return self.classify(text) == VideoIntent.SALES
    
    def is_service_intent(self, text: str) -> bool:
        """Check if text indicates service intent"""
        return self.classify(text) == VideoIntent.SERVICE
    
    def extract_vehicle_info(self, text: str) -> dict:
        """
        Extract vehicle information from text
        
        Returns:
            Dictionary with year, make, model if found
        """
        result = {
            "year": None,
            "make": None,
            "model": None,
        }
        
        # Try to extract year (4-digit number between 1990-2030)
        year_match = re.search(r'\b(19\d{2}|20[0-3]\d)\b', text)
        if year_match:
            result["year"] = int(year_match.group(1))
        
        # Common makes (simplified list)
        makes = [
            "toyota", "honda", "ford", "chevrolet", "chevy", "nissan",
            "hyundai", "kia", "mazda", "subaru", "volkswagen", "vw",
            "bmw", "mercedes", "audi", "lexus", "acura", "infiniti",
            "cadillac", "gmc", "jeep", "ram", "dodge", "chrysler"
        ]
        
        text_lower = text.lower()
        for make in makes:
            if re.search(rf'\b{make}\b', text_lower):
                result["make"] = make.title()
                if make == "chevy":
                    result["make"] = "Chevrolet"
                elif make == "vw":
                    result["make"] = "Volkswagen"
                break
        
        # Try to extract model (word after make)
        if result["make"]:
            make_pattern = result["make"].lower()
            if make_pattern == "chevrolet":
                make_pattern = "(?:chevrolet|chevy)"
            elif make_pattern == "volkswagen":
                make_pattern = "(?:volkswagen|vw)"
            
            model_match = re.search(
                rf'\b{make_pattern}\s+([a-z0-9\-]+)\b',
                text_lower,
                re.IGNORECASE
            )
            if model_match:
                result["model"] = model_match.group(1).title()
        
        return result
    
    def extract_service_info(self, text: str) -> dict:
        """
        Extract service information from text
        
        Returns:
            Dictionary with service type and details
        """
        result = {
            "service_type": None,
            "seasonal": None,
        }
        
        text_lower = text.lower()
        
        # Check for service types
        service_types = {
            "oil change": ["oil change", "oil service"],
            "tire service": ["tire", "tires", "tire rotation", "tire replacement"],
            "brake service": ["brake", "brakes"],
            "maintenance": ["maintenance", "tune-up", "inspection"],
            "seasonal prep": ["winter prep", "summer prep", "seasonal"],
            "diagnostic": ["diagnostic", "diagnosis", "check engine"],
            "battery": ["battery"],
            "alignment": ["alignment"],
        }
        
        for service_name, keywords in service_types.items():
            if any(keyword in text_lower for keyword in keywords):
                result["service_type"] = service_name
                break
        
        # Check for seasonal focus
        if "winter" in text_lower:
            result["seasonal"] = "winter"
        elif "summer" in text_lower:
            result["seasonal"] = "summer"
        
        return result
    
    def extract_tone(self, text: str) -> Optional[str]:
        """Extract desired tone from text"""
        text_lower = text.lower()
        
        tones = {
            "professional": ["professional", "corporate", "business", "formal"],
            "friendly": ["friendly", "warm", "welcoming", "approachable", "family"],
            "dynamic": ["dynamic", "exciting", "energetic", "fast-paced"],
            "luxury": ["luxury", "premium", "high-end", "sophisticated", "elegant"],
            "casual": ["casual", "relaxed", "laid-back", "easy-going"],
        }
        
        for tone_name, keywords in tones.items():
            if any(keyword in text_lower for keyword in keywords):
                return tone_name
        
        return None
    
    def extract_duration(self, text: str) -> Optional[int]:
        """Extract desired video duration in seconds"""
        # Look for patterns like "30 seconds", "1 minute", etc.
        
        # Seconds
        seconds_match = re.search(r'(\d+)\s*(?:second|sec)s?', text, re.IGNORECASE)
        if seconds_match:
            return int(seconds_match.group(1))
        
        # Minutes
        minutes_match = re.search(r'(\d+)\s*(?:minute|min)s?', text, re.IGNORECASE)
        if minutes_match:
            return int(minutes_match.group(1)) * 60
        
        return None
