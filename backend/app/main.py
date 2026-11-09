import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.routes import router as api_router

app = FastAPI(
    title="Relay: Evidence-Linked Knowledge Handover Engine",
    description="Backend API for Team SoloStack - CodersInPune Hackathon 2026 Round 2",
    version="2.0.0"
)

# Enable CORS for local and web development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include core workflow endpoints
app.include_router(api_router, prefix="/api")

# Serve the frontend client directly
FRONTEND_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "index.html"))

@app.get("/")
async def serve_index():
    if os.path.exists(FRONTEND_FILE):
        return FileResponse(FRONTEND_FILE)
    return {
        "message": "Relay Backend API online. Frontend index.html not found.",
        "team": "SoloStack"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
