"""
Helper Utilities

General helper functions for the application.
"""

import os
import re
import uuid
from datetime import datetime
from typing import Optional


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string (e.g., "1m 30s" or "45s")
    """
    if seconds < 60:
        return f"{int(seconds)}s"
    
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    
    if remaining_seconds == 0:
        return f"{minutes}m"
    
    return f"{minutes}m {remaining_seconds}s"


def format_file_size(bytes_size: int) -> str:
    """
    Format file size in bytes to human-readable string
    
    Args:
        bytes_size: Size in bytes
        
    Returns:
        Formatted string (e.g., "15.2 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"


def generate_filename(
    prefix: str = "video",
    extension: str = "mp4",
    include_timestamp: bool = True,
) -> str:
    """
    Generate a unique filename
    
    Args:
        prefix: Filename prefix
        extension: File extension
        include_timestamp: Whether to include timestamp
        
    Returns:
        Generated filename
    """
    if include_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{extension}"
    return f"{prefix}.{extension}"


def ensure_directory(directory_path: str) -> str:
    """
    Ensure directory exists, create if it doesn't
    
    Args:
        directory_path: Path to directory
        
    Returns:
        Absolute path to directory
    """
    abs_path = os.path.abspath(directory_path)
    os.makedirs(abs_path, exist_ok=True)
    return abs_path


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def parse_duration_string(duration_str: str) -> Optional[int]:
    """
    Parse duration string to seconds
    
    Args:
        duration_str: Duration string (e.g., "30s", "1m", "1:30")
        
    Returns:
        Duration in seconds or None if invalid
    """
    duration_str = duration_str.strip().lower()
    
    # Handle seconds format (e.g., "30s")
    if duration_str.endswith('s'):
        try:
            return int(duration_str[:-1])
        except ValueError:
            return None
    
    # Handle minutes format (e.g., "1m")
    if duration_str.endswith('m'):
        try:
            return int(duration_str[:-1]) * 60
        except ValueError:
            return None
    
    # Handle MM:SS format (e.g., "1:30")
    if ':' in duration_str:
        parts = duration_str.split(':')
        if len(parts) == 2:
            try:
                minutes = int(parts[0])
                seconds = int(parts[1])
                return minutes * 60 + seconds
            except ValueError:
                return None
    
    # Try parsing as plain integer (assume seconds)
    try:
        return int(duration_str)
    except ValueError:
        return None


def format_price(price: float, include_symbol: bool = True) -> str:
    """
    Format price for display
    
    Args:
        price: Price value
        include_symbol: Whether to include $ symbol
        
    Returns:
        Formatted price string
    """
    symbol = "$" if include_symbol else ""
    return f"{symbol}{price:,.2f}"


def extract_numbers(text: str) -> list:
    """
    Extract all numbers from text
    
    Args:
        text: Text to parse
        
    Returns:
        List of numbers found
    """
    pattern = r'\d+(?:\.\d+)?'
    matches = re.findall(pattern, text)
    return [float(m) if '.' in m else int(m) for m in matches]


def generate_session_id() -> str:
    """
    Generate a unique session ID
    
    Returns:
        Session ID string
    """
    return str(uuid.uuid4())


def get_timestamp() -> str:
    """
    Get current timestamp as string
    
    Returns:
        Timestamp in ISO format
    """
    return datetime.now().isoformat()


def safe_get(dictionary: dict, *keys, default=None):
    """
    Safely get nested dictionary value
    
    Args:
        dictionary: Dictionary to search
        *keys: Keys to traverse
        default: Default value if not found
        
    Returns:
        Value or default
    """
    result = dictionary
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key)
            if result is None:
                return default
        else:
            return default
    return result


def merge_dicts(*dicts):
    """
    Merge multiple dictionaries
    
    Args:
        *dicts: Dictionaries to merge
        
    Returns:
        Merged dictionary
    """
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result


def chunk_list(lst: list, chunk_size: int) -> list:
    """
    Split list into chunks
    
    Args:
        lst: List to chunk
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def clean_whitespace(text: str) -> str:
    """
    Clean excessive whitespace from text
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    return text.strip()
