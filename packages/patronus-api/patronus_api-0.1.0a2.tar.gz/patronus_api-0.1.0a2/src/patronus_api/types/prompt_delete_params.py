# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["PromptDeleteParams"]


class PromptDeleteParams(TypedDict, total=False):
    project_id: Optional[str]
    """Project ID containing the prompt"""

    project_name: Optional[str]
    """Project name containing the prompt"""
