from typing import Literal

from pydantic import BaseModel, Field

from .date_info import DateInfo
from .user import PartialUser


class VerificationUnverified(BaseModel):
    """未検証状態のverification"""

    state: Literal["unverified"] = Field("unverified", description="検証状態")
    date: None = Field(None, description="検証日")
    verified_by: None = Field(None, description="検証者")


class VerificationInfo(BaseModel):
    """検証済み/期限切れのverification情報"""

    state: Literal["verified", "expired"] = Field(
        ..., description="検証状態"
    )
    date: DateInfo | None = Field(None, description="検証日")
    verified_by: PartialUser | None = Field(None, description="検証者")


Verification = VerificationUnverified | VerificationInfo
"""Notionのverification値"""
