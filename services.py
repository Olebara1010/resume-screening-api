"""
Business logic layer: content moderation, job search/filtering,
and the recommendation-ranking algorithm.

Kept separate from the route handlers (routes.py) so the logic is
independently testable and the API layer stays thin.
"""

from typing import List, Optional
from storage import store

BANNED_KEYWORD = "banned"


def is_content_flagged(filename: str, content: str = "") -> bool:
    """
    Simulated content moderation check.

    Returns True if the banned keyword appears in the filename or
    the attachment content (case-insensitive), which the route layer
    uses to reject the upload with a 400 error.
    """
    haystack = f"{filename} {content}".lower()
    return BANNED_KEYWORD in haystack


def search_jobs(keywords: Optional[str] = None, min_experience: Optional[int] = None) -> List[dict]:
    """
    Filter stored jobs by keyword (matched against title or description)
    and by a minimum experience threshold.

    - keywords: comma-separated string, e.g. "python,backend"
    - min_experience: candidate's years of experience; a job matches if
      the job's min_experience requirement is <= this value
    """
    jobs = store.get_all_jobs()

    if keywords:
        keyword_list = [k.strip().lower() for k in keywords.split(",") if k.strip()]
        if keyword_list:
            jobs = [
                job for job in jobs
                if any(
                    kw in job["title"].lower() or kw in job["description"].lower()
                    for kw in keyword_list
                )
            ]

    if min_experience is not None:
        jobs = [job for job in jobs if job["min_experience"] <= min_experience]

    return jobs


def get_recommendations(resume_id: str) -> List[dict]:
    """
    Return job listings that match a candidate's resume, ranked by the
    number of overlapping skills (descending).

    A job qualifies if:
      - the candidate's years_of_experience >= the job's min_experience, AND
      - at least one required skill overlaps with the candidate's skills
    """
    resume = store.get_resume(resume_id)
    if resume is None:
        return []

    candidate_skills = {s.lower() for s in resume["technical_skills"]}
    candidate_experience = resume["years_of_experience"]

    results = []
    for job in store.get_all_jobs():
        if candidate_experience < job["min_experience"]:
            continue

        job_skills = {s.lower() for s in job["required_skills"]}
        matched = candidate_skills & job_skills

        if matched:
            results.append({
                **job,
                "matched_skills": sorted(matched),
                "matched_skill_count": len(matched),
            })

    results.sort(key=lambda r: r["matched_skill_count"], reverse=True)
    return results
