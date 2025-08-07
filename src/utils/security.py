"""
Security utilities for safe file operations and data handling
"""

import os
import html
import json
from pathlib import Path
from typing import Any, Dict


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal attacks
    """
    # Remove path components and dangerous characters
    filename = os.path.basename(filename)
    filename = "".join(c for c in filename if c.isalnum() or c in "._-")
    
    # Limit length
    if len(filename) > 255:
        filename = filename[:255]
        
    return filename


def safe_file_write(filepath: Path, content: str, max_size: int = 10*1024*1024) -> bool:
    """
    Safely write content to file with validation
    """
    try:
        # Validate file size
        if len(content.encode('utf-8')) > max_size:
            raise ValueError(f"Content exceeds maximum size of {max_size} bytes")
            
        # Ensure parent directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return True
        
    except (OSError, ValueError) as e:
        print(f"Error writing file {filepath}: {e}")
        return False


def sanitize_json_for_html(data: Dict[str, Any]) -> str:
    """
    Safely serialize JSON data for embedding in HTML
    """
    import numpy as np
    
    def convert_numpy(obj):
        """Convert numpy arrays and types to native Python types"""
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.integer, np.floating)):
            return obj.item()
        elif isinstance(obj, dict):
            return {key: convert_numpy(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy(item) for item in obj]
        else:
            return obj
    
    # Convert numpy types to native Python types
    converted_data = convert_numpy(data)
    
    # Convert to JSON string
    json_str = json.dumps(converted_data)
    
    # Escape for HTML
    escaped_json = html.escape(json_str)
    
    return escaped_json


def validate_data_types(data: Dict[str, Any], schema: Dict[str, type]) -> bool:
    """
    Validate data types against expected schema
    """
    for key, expected_type in schema.items():
        if key not in data:
            return False
        if not isinstance(data[key], expected_type):
            return False
    return True