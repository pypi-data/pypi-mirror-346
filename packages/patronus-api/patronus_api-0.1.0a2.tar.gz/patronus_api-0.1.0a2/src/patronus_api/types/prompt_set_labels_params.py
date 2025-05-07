# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, TypedDict

__all__ = ["PromptSetLabelsParams"]


class PromptSetLabelsParams(TypedDict, total=False):
    labels: Required[List[str]]
    """List of labels to set on the prompt version"""

    version: Required[int]
    """The version number of the prompt to set labels on"""

    project_id: Optional[str]
    """Project ID containing the prompt"""

    project_name: Optional[str]
    """Project name containing the prompt"""
