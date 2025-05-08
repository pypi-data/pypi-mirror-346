# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["TestCaseRead", "Trajectory", "TrajectoryMessage", "TrajectoryToolCall", "TrajectoryToolCallToolOutput"]


class TrajectoryMessage(BaseModel):
    id: str

    content: str

    created_at: datetime

    role: str

    test_case_id: str

    updated_at: Optional[datetime] = None


class TrajectoryToolCallToolOutput(BaseModel):
    id: str

    created_at: datetime

    tool_call_id: str

    output: Optional[object] = None

    updated_at: Optional[datetime] = None


class TrajectoryToolCall(BaseModel):
    id: str

    created_at: datetime

    test_case_id: str

    tool_name: str

    arguments: Optional[object] = None

    tool_output: Optional[TrajectoryToolCallToolOutput] = None

    updated_at: Optional[datetime] = None


class Trajectory(BaseModel):
    id: str

    created_at: datetime

    item_type: Literal["message", "tool_call", "unknown"]
    """Derives the type of the trajectory item."""

    order: int

    test_case_id: str

    message: Optional[TrajectoryMessage] = None

    tool_call: Optional[TrajectoryToolCall] = None

    updated_at: Optional[datetime] = None


class TestCaseRead(BaseModel):
    __test__ = False
    id: str

    created_at: datetime

    expected_output: str

    name: str

    status: str

    user_id: str

    description: Optional[str] = None

    is_active: Optional[bool] = None

    trajectory: Optional[List[Trajectory]] = None

    updated_at: Optional[datetime] = None

    validation_criteria: Optional[List[str]] = None
