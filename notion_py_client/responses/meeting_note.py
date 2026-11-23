"""Responses for full-page meeting note endpoints."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, StrictBool, StrictStr

from ..blocks.special_blocks import MeetingNotesContent
from ..models.user import PartialUser


class MeetingNotePageBlock(BaseModel):
    """Meeting note returned by the full-page meeting note endpoints.

    This object is a meeting_notes block without a parent. Block retrieve and
    query responses still use MeetingNotesBlock.
    """

    object: Literal["block"] = Field("block", description="オブジェクトタイプ")
    id: StrictStr = Field(..., description="会議メモブロックID")
    type: Literal["meeting_notes"] = Field(
        "meeting_notes", description="ブロックタイプ"
    )
    meeting_notes: MeetingNotesContent = Field(..., description="会議メモコンテンツ")
    created_time: StrictStr = Field(..., description="作成日時")
    last_edited_time: StrictStr = Field(..., description="最終編集日時")
    created_by: PartialUser = Field(..., description="作成者")
    last_edited_by: PartialUser = Field(..., description="最終編集者")
    has_children: StrictBool = Field(..., description="子ブロックの有無")
    in_trash: StrictBool = Field(..., description="ゴミ箱フラグ")


class CreateMeetingNotePageResponse(BaseModel):
    """POST /v1/meeting_notes のレスポンス."""

    object: Literal["meeting_note_page_result"] = Field(
        ..., description="オブジェクトタイプ"
    )
    meeting_note: MeetingNotePageBlock = Field(..., description="会議メモ")
    created: StrictBool = Field(..., description="新しい会議メモを作成したか")


class LinkMeetingNotePageResponse(BaseModel):
    """PATCH /v1/meeting_notes/{meeting_note_id} のレスポンス."""

    object: Literal["meeting_note_page_result"] = Field(
        ..., description="オブジェクトタイプ"
    )
    meeting_note: MeetingNotePageBlock = Field(..., description="会議メモ")
    other_meeting_note_ids: list[StrictStr] = Field(
        ..., description="同じイベントに紐づく他の会議メモID"
    )
