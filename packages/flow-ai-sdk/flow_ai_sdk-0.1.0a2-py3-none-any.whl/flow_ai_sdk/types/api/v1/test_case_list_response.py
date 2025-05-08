# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .test_case_read import TestCaseRead

__all__ = ["TestCaseListResponse"]

TestCaseListResponse: TypeAlias = List[TestCaseRead]
