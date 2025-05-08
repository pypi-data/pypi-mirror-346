# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["PromptListResponse", "Prompt"]


class Prompt(BaseModel):
    id: str

    body: str
    """The actual content of the prompt"""

    created_at: datetime
    """Timestamp when this prompt version was created"""

    labels: List[str]
    """List of labels associated with this prompt version"""

    name: str
    """Unique name for the prompt, used to group different versions"""

    project_id: str
    """ID of the project this prompt belongs to"""

    version: int
    """Version number of the prompt, starting from 1"""

    description: Optional[str] = None
    """Optional description of the prompt's purpose or usage"""


class PromptListResponse(BaseModel):
    prompts: List[Prompt]
    """List of prompts matching the filter criteria"""
