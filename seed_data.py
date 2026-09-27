"""
Sample data script — inserts 3 jobs and 2 resumes via the running API
so you can immediately test /jobs, /resumes, and /recommendations.

Usage (with the server already running on localhost:8000):
    python seed_data.py
"""

import requests

BASE_URL = "http://localhost:8000"
HEADERS = {"X-API-Key": "demo-api-key-123"}


def seed():
    jobs = [
        {
            "title": "Backend Engineer",
            "description": "Build and maintain REST APIs using Python and FastAPI.",
            "required_skills": ["python", "fastapi", "sql"],
            "min_experience": 2,
        },
        {
            "title": "Frontend Developer",
            "description": "Develop responsive UIs using React and TypeScript.",
            "required_skills": ["javascript", "react", "css"],
            "min_experience": 1,
        },
        {
            "title": "Data Analyst",
            "description": "Analyze datasets and build dashboards using Python and SQL.",
            "required_skills": ["python", "sql", "excel"],
            "min_experience": 0,
        },
    ]

    resumes = [
        {
            "name": "Ada Lovelace",
            "technical_skills": ["python", "fastapi", "sql"],
            "years_of_experience": 3,
            "resume_attachment_name": "ada_resume.pdf",
            "resume_attachment_content": "Experienced backend engineer skilled in Python and SQL.",
        },
        {
            "name": "Grace Hopper",
            "technical_skills": ["javascript", "react", "css"],
            "years_of_experience": 1,
            "resume_attachment_name": "grace_resume.pdf",
            "resume_attachment_content": "Frontend developer with React experience.",
        },
    ]

    print("Seeding jobs...")
    for job in jobs:
        resp = requests.post(f"{BASE_URL}/jobs", json=job, headers=HEADERS)
        print(f"  {resp.status_code} -> {job['title']}")

    print("\nSeeding resumes...")
    for resume in resumes:
        resp = requests.post(f"{BASE_URL}/resumes", json=resume, headers=HEADERS)
        print(f"  {resp.status_code} -> {resume['name']}")
        if resp.status_code == 201:
            print(f"    resume_id: {resp.json()['resume_id']}")


if __name__ == "__main__":
    seed()
