"""
Simple in-memory storage layer.

In a production system this would be swapped for a real database
(PostgreSQL, MongoDB, etc.) — the service layer only depends on the
functions below, so the storage backend can be swapped without
touching business logic.
"""

import uuid
from typing import Dict, List, Optional


class InMemoryStore:
    def __init__(self):
        self.resumes: Dict[str, dict] = {}
        self.jobs: Dict[str, dict] = {}

    # ---------- Resumes ----------
    def add_resume(self, resume_data: dict) -> str:
        resume_id = str(uuid.uuid4())
        self.resumes[resume_id] = {"resume_id": resume_id, **resume_data}
        return resume_id

    def get_resume(self, resume_id: str) -> Optional[dict]:
        return self.resumes.get(resume_id)

    # ---------- Jobs ----------
    def add_job(self, job_data: dict) -> str:
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = {"job_id": job_id, **job_data}
        return job_id

    def get_all_jobs(self) -> List[dict]:
        return list(self.jobs.values())

    def get_job(self, job_id: str) -> Optional[dict]:
        return self.jobs.get(job_id)


# Single shared instance used across the app (simulates a DB connection)
store = InMemoryStore()
