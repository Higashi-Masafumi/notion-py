"""
タイムスタンプフィルター定義

created_time、last_edited_timeに対するフィルター条件。
TypedDict を使用して公式 Notion API 仕様に準拠。

公式TypeScript定義:
type TimestampCreatedTimeFilter = {
  created_time: DatePropertyFilter
  timestamp: "created_time"
  type?: "created_time"
}

type TimestampLastEditedTimeFilter = {
  last_edited_time: DatePropertyFilter
  timestamp: "last_edited_time"
  type?: "last_edited_time"
}

type TimestampFilter =
  | TimestampCreatedTimeFilter
  | TimestampLastEditedTimeFilter
"""

from typing import Literal, NotRequired, TypedDict, Union

from .date_filters import DatePropertyFilter


# ============================================================================
# Timestamp Filters
# ============================================================================


class TimestampCreatedTimeFilter(TypedDict):
    """作成日時タイムスタンプフィルター

    Examples:
        ```python
        filter: TimestampCreatedTimeFilter = {
            "timestamp": "created_time",
            "created_time": {"past_week": {}}
        }
        ```
    """

    timestamp: Literal["created_time"]
    created_time: DatePropertyFilter
    type: NotRequired[Literal["created_time"]]


class TimestampLastEditedTimeFilter(TypedDict):
    """最終編集日時タイムスタンプフィルター

    Examples:
        ```python
        filter: TimestampLastEditedTimeFilter = {
            "timestamp": "last_edited_time",
            "last_edited_time": {"after": "2025-01-01"}
        }
        ```
    """

    timestamp: Literal["last_edited_time"]
    last_edited_time: DatePropertyFilter
    type: NotRequired[Literal["last_edited_time"]]


# Matches TypeScript: type TimestampFilter
TimestampFilter = Union[
    TimestampCreatedTimeFilter,
    TimestampLastEditedTimeFilter,
]
