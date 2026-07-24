"""Main application entry point for the FastAPI app."""

from fastapi import FastAPI

from urls.task import task_router

app = FastAPI()


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


app.router.include_router(prefix="/api", router=task_router)
