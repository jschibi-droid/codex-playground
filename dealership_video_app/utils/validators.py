"""
Input Validation Utilities

Validates user inputs and file uploads.
"""

import os
import re
from typing import Optional, Tuple


class ValidationError(Exception):
    """Raised when validation fails"""
    pass


def validate_input(
    text: str,
    min_length: int = 1,
    max_length: int = 1000,
    allow_empty: bool = False
) -> Tuple[bool, Optional[str]]:
    """
    Validate text input
    
    Args:
        text: Input text to validate
        min_length: Minimum required length
        max_length: Maximum allowed length
        allow_empty: Whether to allow empty input
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text or text.strip() == "":
        if allow_empty:
            return True, None
        return False, "Input cannot be empty"
    
    text_clean = text.strip()
    
    if len(text_clean) < min_length:
        return False, f"Input must be at least {min_length} characters"
    
    if len(text_clean) > max_length:
        return False, f"Input cannot exceed {max_length} characters"
    
    return True, None


def validate_video_file(
    file_path: str,
    max_size_mb: int = 500
) -> Tuple[bool, Optional[str]]:
    """
    Validate video file
    
    Args:
        file_path: Path to video file
        max_size_mb: Maximum file size in MB
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if file exists
    if not os.path.exists(file_path):
        return False, "File does not exist"
    
    # Check if it's a file (not a directory)
    if not os.path.isfile(file_path):
        return False, "Path is not a file"
    
    # Check file extension
    valid_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext not in valid_extensions:
        return False, f"Invalid file format. Supported: {', '.join(valid_extensions)}"
    
    # Check file size
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > max_size_mb:
        return False, f"File size ({file_size_mb:.1f}MB) exceeds maximum ({max_size_mb}MB)"
    
    return True, None


def validate_duration(duration: int, min_duration: int = 5, max_duration: int = 60) -> Tuple[bool, Optional[str]]:
    """
    Validate video duration
    
    Args:
        duration: Duration in seconds
        min_duration: Minimum duration
        max_duration: Maximum duration
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if duration < min_duration:
        return False, f"Duration must be at least {min_duration} seconds"
    
    if duration > max_duration:
        return False, f"Duration cannot exceed {max_duration} seconds"
    
    return True, None


def validate_url(url: str) -> Tuple[bool, Optional[str]]:
    """
    Validate URL format
    
    Args:
        url: URL to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    
    if not url_pattern.match(url):
        return False, "Invalid URL format"
    
    return True, None


def validate_price(price_str: str) -> Tuple[bool, Optional[str]]:
    """
    Validate price format
    
    Args:
        price_str: Price string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Remove common price formatting
    price_clean = price_str.replace('$', '').replace(',', '').strip()
    
    try:
        price_value = float(price_clean)
        if price_value < 0:
            return False, "Price cannot be negative"
        if price_value > 1000000:
            return False, "Price exceeds reasonable limits"
        return True, None
    except ValueError:
        return False, "Invalid price format"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to remove invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Limit length
    if len(filename) > 200:
        name, ext = os.path.splitext(filename)
        filename = name[:195] + ext
    
    return filename


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    if not email_pattern.match(email):
        return False, "Invalid email format"
    
    return True, None


def validate_phone(phone: str) -> Tuple[bool, Optional[str]]:
    """
    Validate phone number format
    
    Args:
        phone: Phone number to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Remove common formatting characters
    phone_clean = re.sub(r'[\s\-\(\)\.]+', '', phone)
    
    # Check if it's all digits
    if not phone_clean.isdigit():
        return False, "Phone number must contain only digits"
    
    # Check length (US format)
    if len(phone_clean) != 10:
        return False, "Phone number must be 10 digits"
    
    return True, None
