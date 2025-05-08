# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .batch_read import BatchRead

__all__ = ["BatchListByAPIKeyResponse"]

BatchListByAPIKeyResponse: TypeAlias = List[BatchRead]
