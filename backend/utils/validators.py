from fastapi import HTTPException
import re

def validate_text_input(text: str, max_length: int = 500) -> str:
    """Validate and sanitize text input"""
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    text = text.strip()
    if len(text) > max_length:
        raise HTTPException(status_code=400, detail=f"Text too long. Max {max_length} characters")
    
    # Remove potentially harmful characters
    text = re.sub(r'[<>"\']', '', text)
    return text

def validate_file_size(file_size: int, max_size: int = 10 * 1024 * 1024) -> None:
    """Validate file size (default 10MB)"""
    if file_size > max_size:
        raise HTTPException(status_code=400, detail="File too large")

def validate_voice_id(voice_id: str) -> str:
    """Validate voice ID format"""
    if not voice_id or len(voice_id) < 10:
        raise HTTPException(status_code=400, detail="Invalid voice ID")
    return voice_id