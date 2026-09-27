"""
Data models for the Resume Screening & Job Recommendation API.

Uses Pydantic for request/response validation and simple Python
dataclasses-style dicts for in-memory storage.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class ResumeCreate(BaseModel):
    """Payload for creating a new resume."""
    name: str = Field(..., description="Candidate's full name")
    technical_skills: List[str] = Field(..., description="List of technical skills")
    years_of_experience: int = Field(..., ge=0, description="Years of professional experience")
    resume_attachment_name: str = Field(..., description="Filename of the resume attachment")
    resume_attachment_content: Optional[str] = Field(
        default="", description="Text content of the attachment (for moderation simulation)"
    )


class ResumeResponse(BaseModel):
    """Response returned after successfully creating a resume."""
    resume_id: str
    name: str
    technical_skills: List[str]
    years_of_experience: int


class JobCreate(BaseModel):
    """Payload for creating a new job listing."""
    title: str
    description: str
    required_skills: List[str] = Field(..., description="Skills required for the job")
    min_experience: int = Field(..., ge=0, description="Minimum years of experience required")


class JobResponse(BaseModel):
    """Response representing a stored job listing."""
    job_id: str
    title: str
    description: str
    required_skills: List[str]
    min_experience: int


class RecommendationResponse(BaseModel):
    """A job recommendation, including how many skills matched."""
    job_id: str
    title: str
    description: str
    required_skills: List[str]
    min_experience: int
    matched_skills: List[str]
    matched_skill_count: int
