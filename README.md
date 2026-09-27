# Resume Screening & Job Recommendation API

A backend API for a simplified automated resume screening and job
recommendation system, built with **FastAPI**. Accepts candidate resume
data, stores job listings, provides keyword-based job search, and
recommends jobs ranked by skill overlap.

## Design Overview

The code is split into four layers to keep things modular and scalable:

- **`models.py`** — Pydantic request/response schemas (validation + typing)
- **`storage.py`** — in-memory data store (`InMemoryStore`), standing in for
  a real database. Swappable behind the same interface if a real DB
  (PostgreSQL, MongoDB, etc.) were introduced later.
- **`services.py`** — business logic: content moderation, job search/filter,
  and the recommendation-ranking algorithm. Kept separate from routes so
  it's independently testable.
- **`routes.py`** — thin FastAPI route handlers that validate input, call
  into services/storage, and shape responses.
- **`main.py`** — application entry point, wires everything together.

Resumes and jobs are each assigned a UUID on creation.

## Running Locally

**1. Install dependencies:**
```bash
pip install -r requirements.txt
```

**2. Start the server:**
```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`.
Interactive docs (Swagger UI) are auto-generated at `http://localhost:8000/docs`.

**3. (Optional) Seed sample data** — inserts 3 jobs and 2 resumes so you
can immediately test search and recommendations:
```bash
python seed_data.py
```

## Running with Docker (Bonus)

```bash
docker build -t resume-api .
docker run -p 8000:8000 resume-api
```

## Authentication (Bonus)

Write endpoints (`POST /resumes`, `POST /jobs`) require an API key via
the `X-API-Key` header. Read endpoints (`GET /jobs`, `GET /recommendations`)
are left public so job search stays open. Demo key:
```
X-API-Key: demo-api-key-123
```
All curl examples below include this header where required.

## Endpoints

### `POST /resumes`
Creates a resume. Simulates a content moderation check: if the string
`"banned"` appears (case-insensitive) in the attachment filename or
content, the request is rejected with a `400`.

```bash
curl -X POST http://localhost:8000/resumes \
  -H "Content-Type: application/json" \
  -H "X-API-Key: demo-api-key-123" \
  -d '{
    "name": "Ada Lovelace",
    "technical_skills": ["python", "fastapi", "sql"],
    "years_of_experience": 3,
    "resume_attachment_name": "ada_resume.pdf",
    "resume_attachment_content": "Experienced backend engineer."
  }'
```

Response (`201`):
```json
{
  "resume_id": "effd7b96-d094-48dd-a209-7545513358de",
  "name": "Ada Lovelace",
  "technical_skills": ["python", "fastapi", "sql"],
  "years_of_experience": 3
}
```

Moderation rejection example (filename contains "banned"):
```bash
curl -X POST http://localhost:8000/resumes \
  -H "Content-Type: application/json" \
  -H "X-API-Key: demo-api-key-123" \
  -d '{
    "name": "Test",
    "technical_skills": ["python"],
    "years_of_experience": 2,
    "resume_attachment_name": "banned_resume.pdf"
  }'
# -> 400 Bad Request
```

### `GET /jobs`
Returns job listings. Supports optional query parameters:
- `keywords` — comma-separated, matched against job title or description
- `min_experience` — candidate's years of experience; returns jobs whose
  requirement is less than or equal to this value

```bash
# All jobs
curl http://localhost:8000/jobs

# Filter by keyword
curl "http://localhost:8000/jobs?keywords=python,backend"

# Filter by experience
curl "http://localhost:8000/jobs?min_experience=2"

# Combine both
curl "http://localhost:8000/jobs?keywords=python&min_experience=2"
```

### `POST /jobs`
Creates a new job listing.

```bash
curl -X POST http://localhost:8000/jobs \
  -H "Content-Type: application/json" \
  -H "X-API-Key: demo-api-key-123" \
  -d '{
    "title": "Backend Engineer",
    "description": "Build and maintain REST APIs using Python and FastAPI.",
    "required_skills": ["python", "fastapi", "sql"],
    "min_experience": 2
  }'
```

### `GET /recommendations/{resume_id}`
Returns job listings that match a resume's skills and experience,
ranked by number of matched skills (descending). A job qualifies if the
candidate's `years_of_experience >= job.min_experience` and at least
one skill overlaps.

```bash
curl http://localhost:8000/recommendations/effd7b96-d094-48dd-a209-7545513358de
```

Response:
```json
[
  {
    "job_id": "d54ec2d6-...",
    "title": "Backend Engineer",
    "description": "Build and maintain REST APIs using Python and FastAPI.",
    "required_skills": ["python", "fastapi", "sql"],
    "min_experience": 2,
    "matched_skills": ["fastapi", "python", "sql"],
    "matched_skill_count": 3
  }
]
```

## Notes

- No frontend is included, per the task scope.
- Data is in-memory and resets whenever the server restarts — swap
  `storage.py`'s `InMemoryStore` for a real database client to persist
  data, without needing to touch `services.py` or `routes.py`.
- Uploaded attachments are simulated as text (filename + content string)
  rather than real file uploads, per the task's simplification notes.
