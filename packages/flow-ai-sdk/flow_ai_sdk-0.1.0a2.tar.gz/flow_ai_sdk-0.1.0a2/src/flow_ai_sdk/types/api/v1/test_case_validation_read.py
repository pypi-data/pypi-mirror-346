# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from ...._models import BaseModel

__all__ = ["TestCaseValidationRead", "ItemFeedback"]


class ItemFeedback(BaseModel):
    id: str

    created_at: datetime

    is_correct: bool

    test_case_validation_id: str

    trajectory_item_id: str

    feedback_text: Optional[str] = None

    updated_at: Optional[datetime] = None


class TestCaseValidationRead(BaseModel):
    __test__ = False
    id: str

    created_at: datetime

    is_accepted: bool

    test_case_id: str

    validator_user_id: str

    feedback: Optional[str] = None

    item_feedbacks: Optional[List[ItemFeedback]] = None

    updated_at: Optional[datetime] = None
