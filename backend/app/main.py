import time
import logging
from fastapi import FastAPI, Request
from .routes import chat
from .services.ollama_client import OllamaService
from .config import settings

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger("medgemma-api")

app = FastAPI(title="MedGemma 1.5 Vision Chat API")

# Health Check
@app.get("/health")
async def health_check():
    ollama = OllamaService()
    try:
        models = await ollama.list_models()
        model_available = settings.MODEL_NAME in models
        return {
            "status": "healthy",
            "ollama_connected": True,
            "model_ready": model_available,
            "configured_model": settings.MODEL_NAME
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "ollama_connected": False,
            "error": str(e)
        }

# Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Status: {response.status_code} Duration: {duration:.2f}s"
    )
    return response

# Include Routers
app.include_router(chat.router, prefix="/chat", tags=["chat"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
