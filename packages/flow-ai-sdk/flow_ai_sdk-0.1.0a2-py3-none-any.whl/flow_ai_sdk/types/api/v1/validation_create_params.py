# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Required, TypedDict

from .validation_item_feedback_input_param import ValidationItemFeedbackInputParam

__all__ = ["ValidationCreateParams"]


class ValidationCreateParams(TypedDict, total=False):
    is_accepted: Required[bool]

    test_case_id: Required[str]

    feedback: Optional[str]

    item_feedbacks: Optional[Iterable[ValidationItemFeedbackInputParam]]
