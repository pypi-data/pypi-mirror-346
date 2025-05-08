# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import TypedDict

from .validation_item_feedback_input_param import ValidationItemFeedbackInputParam

__all__ = ["ValidationUpdateParams"]


class ValidationUpdateParams(TypedDict, total=False):
    feedback: Optional[str]

    is_accepted: Optional[bool]

    item_feedbacks: Optional[Iterable[ValidationItemFeedbackInputParam]]
