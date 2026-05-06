# MedGemma 1.5 Vision Chat Backend

A production-ready FastAPI backend for medical vision chat using MedGemma 1.5 on Ollama.

## Setup

1. **Ollama**: Ensure Ollama is running and has `medgemma:1.5` (or the configured GGUF) pulled.
2. **Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Run**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Docker

1. **Build** (run from the `backend` directory):
   ```bash
   cd backend
   docker build -t medgemma-backend .
   ```
2. **Run**:
   ```bash
   docker run -d -p 8000:8000 \
     -e OLLAMA_BASE_URL="http://host.docker.internal:11434" \
     medgemma-backend
   ```
   _Note: On Docker Desktop (Mac/Windows), use `host.docker.internal` to reach services running on your host machine (like Ollama)._

## API Usage

### Health Check

`GET /health`

### Text Chat

`POST /chat/text`

- Payload: `{"message": "What are common signs of iron deficiency?"}`

### Image Chat

`POST /chat/image`

- Form Data:
  - `message`: "Describe what you see in this image."
  - `image`: [File]
  - `ocr_text`: (Optional) "Pre-extracted OCR text"

## Guards

- **No Diagnosis**: The model is restricted from providing definitive diagnoses.
- **No Treatment**: The model will not recommend specific medications or treatments.
- **Image Priority**: Visual evidence is prioritized over text/OCR.
