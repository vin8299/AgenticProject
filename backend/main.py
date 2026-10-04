from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.ai_service import ask_ai


app = FastAPI(
    title="eCommerceSupport-AI"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):

    session_id: str
    message: str


@app.get("/")
def home():

    return {
        "service": "eCommerceSupport-AI",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    answer = ask_ai(
        request.session_id,
        request.message
    )

    return {
        "session_id": request.session_id,
        "reply": answer
    }