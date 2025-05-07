# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["PromptListParams"]


class PromptListParams(TypedDict, total=False):
    id: Optional[str]
    """Filter prompts by specific UUID"""

    label: Optional[str]
    """Filter prompts by label"""

    name: Optional[str]
    """Filter prompts by name"""

    project_id: Optional[str]
    """Filter prompts by project ID"""

    project_name: Optional[str]
    """Filter prompts by project name"""

    version: Optional[int]
    """Filter prompts by version number"""
