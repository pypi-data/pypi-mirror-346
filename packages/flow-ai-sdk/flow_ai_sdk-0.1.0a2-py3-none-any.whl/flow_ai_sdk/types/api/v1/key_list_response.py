# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .api_key_info import APIKeyInfo

__all__ = ["KeyListResponse"]

KeyListResponse: TypeAlias = List[APIKeyInfo]
