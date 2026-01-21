from pydantic import BaseModel, Field
from typing import Optional, List

class TextChatRequest(BaseModel):
    message: str = Field(..., description="User message content")
    conversation_id: Optional[str] = Field(None, description="Optional conversation identifier")

class ImageChatRequest(BaseModel):
    message: str = Field(..., description="User message content")
    ocr_text: Optional[str] = Field(None, description="Optional OCR text from the image")

class ChatResponseMetadata(BaseModel):
    model: str
    inference_time: float
    image_used: bool

class ChatResponse(BaseModel):
    content: str
    metadata: ChatResponseMetadata
