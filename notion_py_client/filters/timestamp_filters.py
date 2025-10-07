"""
タイムスタンプフィルター定義

created_time、last_edited_timeに対するフィルター条件。
公式TypeScript SDKのTimestampFilter型に対応。
"""

from typing import Literal, Union

from pydantic import BaseModel, Field

from .date_filters import DatePropertyFilter


class TimestampCreatedTimeFilter(BaseModel):
    """作成日時タイムスタンプフィルター (公式SDK: { timestamp: "created_time", created_time: DatePropertyFilter })"""

    timestamp: Literal["created_time"] = Field(
        default="created_time", description="タイムスタンプタイプ"
    )
    created_time: DatePropertyFilter = Field(..., description="作成日時フィルター条件")


class TimestampLastEditedTimeFilter(BaseModel):
    """最終編集日時タイムスタンプフィルター (公式SDK: { timestamp: "last_edited_time", last_edited_time: DatePropertyFilter })"""

    timestamp: Literal["last_edited_time"] = Field(
        default="last_edited_time", description="タイムスタンプタイプ"
    )
    last_edited_time: DatePropertyFilter = Field(
        ..., description="最終編集日時フィルター条件"
    )


# 公式SDK: TimestampFilter = TimestampCreatedTimeFilter | TimestampLastEditedTimeFilter
TimestampFilter = Union[
    TimestampCreatedTimeFilter,
    TimestampLastEditedTimeFilter,
]
