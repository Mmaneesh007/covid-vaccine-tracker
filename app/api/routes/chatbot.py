"""
AI Chatbot endpoints
Provides natural language health assistant
"""
from fastapi import APIRouter, HTTPException, Body
from typing import Optional
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from app.api.models import ChatRequest, ChatResponse
from src.chatbot import get_chatbot_response

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest = Body(..., description="Chat message request")):
    """
    Send a message to the AI health assistant
    
    The chatbot can answer questions about COVID-19 vaccines, safety, side effects,
    and provide vaccination statistics for different countries.
    
    **Supported Languages:**
    - en: English
    - hi: Hindi
    - bn: Bengali
    - ta: Tamil
    - te: Telugu
    
    **Example Questions:**
    - "Is the COVID vaccine safe?"
    - "What are the side effects?"
    - "How many people are vaccinated in India?"
    - "Is the covid vaccine safe?" (Hindi)
    """
    try:
        # Get response from existing chatbot
        response_text = get_chatbot_response(request.message, lang=request.language)
        
        if not response_text:
            response_text = "I'm sorry, I couldn't understand your question. Please try rephrasing."
        
        return ChatResponse(
            message=response_text,
            language=request.language,
            sentiment=None  # Could add sentiment analysis here if needed
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {str(e)}"
        )


@router.get("/chat/languages")
async def get_supported_languages():
    """
    Get list of supported languages for the chatbot
    
    Returns language codes and their names.
    """
    return {
        "languages": [
            {"code": "en", "name": "English"},
            {"code": "hi", "name": "Hindi"},
            {"code": "bn", "name": "Bengali"},
            {"code": "ta", "name": "Tamil"},
            {"code": "te", "name": "Telugu"}
        ]
    }
