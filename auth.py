"""
Simple API key authentication.

Not mandatory per the task spec, but included as the listed bonus.
Checks for a valid key in the `X-API-Key` header. In a real system
this would be looked up from a database/secrets manager rather than
hardcoded — kept simple here since it's a bonus, demo-only feature.
"""

from fastapi import Header, HTTPException
from typing import Optional

VALID_API_KEYS = {"demo-api-key-123"}


def verify_api_key(x_api_key: Optional[str] = Header(default=None)):
    """FastAPI dependency: raises 401 if the API key is missing or invalid."""
    if x_api_key is None or x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")
    return x_api_key
