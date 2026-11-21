from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.uploads import router as uploads_router
from app.routes.projects import router as projects_router

app = FastAPI(title="AI Clipper API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(uploads_router)
app.include_router(projects_router)

@app.get("/health")
def health_check() -> dict[str, str]:
    """Simple check that the backend is running."""
    return {"status": "ok"}