# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["RunCreateParams"]


class RunCreateParams(TypedDict, total=False):
    task_id: Required[Annotated[str, PropertyInfo(alias="taskId")]]
    """The ID of the task to execute"""

    inputs: Dict[str, object]
    """The inputs required for the task"""

    url: str
    """An optional URL to be processed by the task"""
