# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["WhoamiRetrieveResponse", "Caller", "CallerAPIKey", "CallerAPIKeyAccount", "CallerUser", "CallerUserAccount"]


class CallerAPIKeyAccount(BaseModel):
    id: str

    name: str


class CallerAPIKey(BaseModel):
    id: str

    account: CallerAPIKeyAccount


class CallerUserAccount(BaseModel):
    id: str

    name: str

    role: Optional[str] = None

    features_enabled: Optional[List[str]] = None


class CallerUser(BaseModel):
    id: str

    accounts: List[CallerUserAccount]

    is_staff: bool

    sub: str


class Caller(BaseModel):
    api_key: Optional[CallerAPIKey] = None

    user: Optional[CallerUser] = None


class WhoamiRetrieveResponse(BaseModel):
    caller: Caller
