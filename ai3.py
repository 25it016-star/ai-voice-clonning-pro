"""FastAPI server: /api/analyze + serves the frontend."""
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from features import load_audio
from detector import Detector

app = FastAPI(title="Voice Cloning Detection Prototype")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
detector = Detector()


@app.get("/api/health")
def health():
    return {"status": "ok", "mode": detector.mode}


@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    data = await file.read()
    try:
        y = load_audio(data)
    except Exception as e:
        return {"ok": False, "error": f"Could not read audio: {e}"}
    return detector.analyze(y)


FRONTEND = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/", StaticFiles(directory=FRONTEND, html=True), name="frontend")