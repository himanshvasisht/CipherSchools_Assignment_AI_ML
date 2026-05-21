import os
import sys

# Ensure backend and root are in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.append(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app_engine import run_review

app = FastAPI(title="Repository Intelligence & Review Platform API")

# CORS middleware for local frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RepoRequest(BaseModel):
    repo_url: str
    simulate_stress: bool = False

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/review")
def review_repo(req: RepoRequest):
    try:
        result = run_review(req.repo_url, simulate_stress=req.simulate_stress)
        if not result.get("success"):
            return JSONResponse(status_code=400, content=result)
        return result
    except Exception as e:
        print(f"Server error: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )