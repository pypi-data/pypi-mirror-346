# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from ...._models import BaseModel
from .test_case_read import TestCaseRead

__all__ = ["BatchRead"]


class BatchRead(BaseModel):
    id: str

    completed_test_cases: int

    created_at: datetime

    description: str

    name: str

    total_test_cases: int

    user_id: str

    test_cases: Optional[List[TestCaseRead]] = None

    updated_at: Optional[datetime] = None
