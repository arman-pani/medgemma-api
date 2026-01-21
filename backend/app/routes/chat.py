import json
from fastapi import APIRouter, UploadFile, File, Form, Depends
from fastapi.responses import StreamingResponse
from ..schemas.chat import TextChatRequest
from ..services.ollama_client import OllamaService
from ..utils.image import validate_image, encode_image
from ..utils.prompts import format_user_prompt
from typing import Optional

router = APIRouter()
ollama_service = OllamaService()

@router.post("/text")
async def chat_text(request: TextChatRequest):
    """
    Handle text-only chat requests with streaming.
    """
    user_prompt = format_user_prompt(request.message)
    
    async def stream_generator():
        async for chunk in ollama_service.generate_response(user_prompt):
            if "error" in chunk:
                yield f"data: {json.dumps({'error': chunk['error']})}\n\n"
                break
            
            # Ollama SSE style or just chunks
            yield f"data: {json.dumps(chunk)}\n\n"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")

@router.post("/image")
async def chat_image(
    message: str = Form(...),
    ocr_text: Optional[str] = Form(None),
    image: UploadFile = File(...)
):
    """
    Handle image + text chat requests with streaming.
    """
    validate_image(image)
    base64_image = await encode_image(image)
    
    user_prompt = format_user_prompt(message, ocr_text)
    
    async def stream_generator():
        async for chunk in ollama_service.generate_response(user_prompt, images=[base64_image]):
            if "error" in chunk:
                yield f"data: {json.dumps({'error': chunk['error']})}\n\n"
                break
            
            yield f"data: {json.dumps(chunk)}\n\n"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")
