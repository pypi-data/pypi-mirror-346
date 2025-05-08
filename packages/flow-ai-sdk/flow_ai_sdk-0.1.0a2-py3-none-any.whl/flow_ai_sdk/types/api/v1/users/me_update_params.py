# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

__all__ = ["MeUpdateParams"]


class MeUpdateParams(TypedDict, total=False):
    email: Optional[str]

    first_name: Optional[str]

    image_url: Optional[str]

    is_active: Optional[bool]

    last_name: Optional[str]

    preferences: Optional[Dict[str, object]]

    role: Optional[str]

    username: Optional[str]
