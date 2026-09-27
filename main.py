"""
Cloud-Native Resume Screening and Job Recommendation API.

Entry point: wires up the FastAPI app and includes the route router.
Run with:  uvicorn main:app --reload
"""

from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="Resume Screening & Job Recommendation API",
    description=(
        "Accepts candidate resume data, stores job listings, and "
        "recommends jobs based on skill overlap and experience."
    ),
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def root():
    """Simple health-check / welcome endpoint."""
    return {"status": "ok", "message": "Resume Screening API is running."}
