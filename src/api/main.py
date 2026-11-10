
import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.generation.rag_pipeline import ask_nexus

app = FastAPI(
    title="NEXUS AI API",
    description="Intelligent Support and Knowledge System",
    version="1.0.0"
)

logging.basicConfig(level=logging.INFO)

class QuestionRequest(BaseModel):

    question: str = Field(
        min_length=3,
        max_length=1000,
        description="Customer support question"
    )

@app.get("/")
def home():

    return {
        "message": "Welcome to NEXUS AI",
        "status": "running"
    }

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

@app.post("/ask")
def ask_question(request: QuestionRequest):

    try:

        result = ask_nexus(request.question)

        return {
            "success": True,
            "question": result["question"],
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except Exception:

        logging.exception("Error while processing question")

        raise HTTPException(
            status_code=500,
            detail="NEXUS AI could not process your question."
        )
