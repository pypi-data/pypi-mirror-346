# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["PromptCreateRevisionParams"]


class PromptCreateRevisionParams(TypedDict, total=False):
    body: Required[str]
    """New content for the prompt revision"""

    project_id: Optional[str]
    """Project ID containing the prompt"""

    project_name: Optional[str]
    """Project name containing the prompt"""
