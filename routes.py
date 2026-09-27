"""
API route definitions.

All endpoints return JSON, per the spec. Route handlers stay thin —
they validate input, call into services.py / storage.py, and shape
the response.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List

from models import (
    ResumeCreate, ResumeResponse,
    JobCreate, JobResponse,
    RecommendationResponse,
)
from storage import store
from services import is_content_flagged, search_jobs, get_recommendations
from auth import verify_api_key

router = APIRouter()


@router.post("/resumes", response_model=ResumeResponse, status_code=201)
def create_resume(payload: ResumeCreate, api_key: str = Depends(verify_api_key)):
    """
    Accept a candidate's resume data, run a simulated content-moderation
    check on the attachment, store the resume, and return its new ID.
    """
    if is_content_flagged(payload.resume_attachment_name, payload.resume_attachment_content or ""):
        raise HTTPException(
            status_code=400,
            detail="Attachment rejected: content moderation check failed (banned content detected)."
        )

    resume_id = store.add_resume({
        "name": payload.name,
        "technical_skills": payload.technical_skills,
        "years_of_experience": payload.years_of_experience,
    })

    return ResumeResponse(
        resume_id=resume_id,
        name=payload.name,
        technical_skills=payload.technical_skills,
        years_of_experience=payload.years_of_experience,
    )


@router.get("/jobs", response_model=List[JobResponse])
def list_jobs(
    keywords: Optional[str] = Query(None, description="Comma-separated keywords"),
    min_experience: Optional[int] = Query(None, ge=0, description="Candidate's years of experience"),
):
    """
    Return job listings, optionally filtered by keyword (title/description)
    and by minimum experience. If no query params are given, all jobs
    are returned.
    """
    jobs = search_jobs(keywords=keywords, min_experience=min_experience)
    return [JobResponse(**job) for job in jobs]


@router.post("/jobs", response_model=JobResponse, status_code=201)
def create_job(payload: JobCreate, api_key: str = Depends(verify_api_key)):
    """Create and store a new job listing."""
    job_id = store.add_job({
        "title": payload.title,
        "description": payload.description,
        "required_skills": payload.required_skills,
        "min_experience": payload.min_experience,
    })

    return JobResponse(
        job_id=job_id,
        title=payload.title,
        description=payload.description,
        required_skills=payload.required_skills,
        min_experience=payload.min_experience,
    )


@router.get("/recommendations/{resume_id}", response_model=List[RecommendationResponse])
def recommend_jobs(resume_id: str):
    """
    Return job listings recommended for a given resume, ranked by the
    number of matched skills (descending). Requires the candidate's
    experience to meet each job's minimum requirement.
    """
    if store.get_resume(resume_id) is None:
        raise HTTPException(status_code=404, detail=f"Resume '{resume_id}' not found.")

    recommendations = get_recommendations(resume_id)
    return [RecommendationResponse(**rec) for rec in recommendations]
