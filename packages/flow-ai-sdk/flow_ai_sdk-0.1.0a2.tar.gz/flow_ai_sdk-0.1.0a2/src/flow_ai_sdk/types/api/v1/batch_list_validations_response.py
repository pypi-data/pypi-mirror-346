# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .test_case_validation_read import TestCaseValidationRead

__all__ = ["BatchListValidationsResponse"]

BatchListValidationsResponse: TypeAlias = List[TestCaseValidationRead]
