from fastapi import FastAPI

app = FastAPI(title="AI Clipper API", version="0.1.0")


@app.get("/health")
def health_check() -> dict[str, str]:
    """Simple check that the backend is running."""
    return {"status": "ok"}