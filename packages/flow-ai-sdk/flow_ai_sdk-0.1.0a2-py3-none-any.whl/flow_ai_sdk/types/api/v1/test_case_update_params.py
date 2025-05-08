# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import TypedDict

__all__ = ["TestCaseUpdateParams"]


class TestCaseUpdateParams(TypedDict, total=False):
    description: Optional[str]

    expected_output: Optional[str]

    is_active: Optional[bool]

    name: Optional[str]

    status: Optional[str]

    validation_criteria: Optional[List[str]]
