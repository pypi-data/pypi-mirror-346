# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = ["TestCaseCreateParams", "Trajectory", "TrajectoryMessageStepCreate", "TrajectoryToolCallStepCreate"]


class TestCaseCreateParams(TypedDict, total=False):
    expected_output: Required[str]

    name: Required[str]

    status: Required[str]

    description: Optional[str]

    is_active: bool

    trajectory: Iterable[Trajectory]

    validation_criteria: Optional[List[str]]


class TrajectoryMessageStepCreate(TypedDict, total=False):
    content: Required[str]

    order: Required[int]

    role: Required[str]

    type: Literal["message"]


class TrajectoryToolCallStepCreate(TypedDict, total=False):
    order: Required[int]

    tool_name: Required[str]

    arguments: object

    output: object

    type: Literal["tool_call"]


Trajectory: TypeAlias = Union[TrajectoryMessageStepCreate, TrajectoryToolCallStepCreate]
