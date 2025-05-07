# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["PromptUpdateParams"]


class PromptUpdateParams(TypedDict, total=False):
    project_id: Optional[str]
    """Project ID containing the prompt"""

    project_name: Optional[str]
    """Project name containing the prompt"""

    description: Optional[str]
    """New description for the prompt"""

    body_name: Annotated[Optional[str], PropertyInfo(alias="name")]
    """
    New name for the prompt, must contain only alphanumeric characters, hyphens, and
    underscores
    """
