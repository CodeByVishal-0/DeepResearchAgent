from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio
import json
import sys
import os

# Add the project directory to path so pipeline can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(title="Deep Research AI", version="1.0.0")

class ResearchRequest(BaseModel):
    topic: str

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("templates/index.html", encoding="utf-8") as f:
        return f.read()

@app.post("/api/research")
async def run_research(request: ResearchRequest):
    """Run the full research pipeline and return results."""
    try:
        from pipeline import run_research_pipeline
        result = run_research_pipeline(request.topic)
        return {
            "success": True,
            "topic": request.topic,
            "search_result": result.get("search_result", ""),
            "scrapped_content": result.get("scrapped_content", ""),
            "report": result.get("report", ""),
            "feedback": result.get("feedback", "")
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "Deep Research AI"}