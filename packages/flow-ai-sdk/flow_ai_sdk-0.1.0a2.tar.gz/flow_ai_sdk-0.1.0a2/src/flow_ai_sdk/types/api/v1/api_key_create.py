# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ...._models import BaseModel
from .api_key_info import APIKeyInfo

__all__ = ["APIKeyCreate"]


class APIKeyCreate(BaseModel):
    api_key: str
    """The full, unhashed API key. Store this securely!"""

    key_info: APIKeyInfo

    message: Optional[str] = None
    """User message"""
