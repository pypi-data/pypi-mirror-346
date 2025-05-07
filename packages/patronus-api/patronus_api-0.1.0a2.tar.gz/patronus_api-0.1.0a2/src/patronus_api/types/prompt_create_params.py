# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, TypedDict

__all__ = ["PromptCreateParams"]


class PromptCreateParams(TypedDict, total=False):
    body: Required[str]
    """Content of the prompt"""

    name: Required[str]
    """
    Name for the prompt, must contain only alphanumeric characters, hyphens, and
    underscores
    """

    description: Optional[str]
    """Optional description of the prompt's purpose or usage"""

    labels: List[str]
    """Optional labels to associate with this prompt version"""

    project_id: Optional[str]
    """ID of the project to create the prompt in"""

    project_name: Optional[str]
    """Name of the project to create the prompt in"""
