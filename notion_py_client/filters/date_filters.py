"""
日付フィルター定義

日付プロパティに対するフィルター条件。
TypedDict を使用して公式 Notion API 仕様に準拠。

公式TypeScript定義:
type DatePropertyFilter =
  | { equals: string }
  | { before: string }
  | { after: string }
  | { on_or_before: string }
  | { on_or_after: string }
  | { this_week: EmptyObject }
  | { past_week: EmptyObject }
  | { past_month: EmptyObject }
  | { past_year: EmptyObject }
  | { next_week: EmptyObject }
  | { next_month: EmptyObject }
  | { next_year: EmptyObject }
  | ExistencePropertyFilter
"""

from typing import TypedDict, Union

from .base_filters import ExistencePropertyFilter


# EmptyObject for relative date filters
class EmptyObject(TypedDict):
    """空オブジェクト（相対日付フィルター用）"""

    pass


# ============================================================================
# Date Property Filters
# ============================================================================


class DateFilterEquals(TypedDict):
    """日付が等しい

    Examples:
        ```python
        filter: DateFilterEquals = {"equals": "2025-01-01"}
        ```
    """

    equals: str


class DateFilterBefore(TypedDict):
    """日付より前"""

    before: str


class DateFilterAfter(TypedDict):
    """日付より後"""

    after: str


class DateFilterOnOrBefore(TypedDict):
    """日付以前"""

    on_or_before: str


class DateFilterOnOrAfter(TypedDict):
    """日付以降"""

    on_or_after: str


class DateFilterThisWeek(TypedDict):
    """今週

    Examples:
        ```python
        filter: DateFilterThisWeek = {"this_week": {}}
        ```
    """

    this_week: EmptyObject


class DateFilterPastWeek(TypedDict):
    """先週"""

    past_week: EmptyObject


class DateFilterPastMonth(TypedDict):
    """先月"""

    past_month: EmptyObject


class DateFilterPastYear(TypedDict):
    """昨年"""

    past_year: EmptyObject


class DateFilterNextWeek(TypedDict):
    """来週"""

    next_week: EmptyObject


class DateFilterNextMonth(TypedDict):
    """来月"""

    next_month: EmptyObject


class DateFilterNextYear(TypedDict):
    """来年"""

    next_year: EmptyObject


# Matches TypeScript DatePropertyFilter
DatePropertyFilter = Union[
    DateFilterEquals,
    DateFilterBefore,
    DateFilterAfter,
    DateFilterOnOrBefore,
    DateFilterOnOrAfter,
    DateFilterThisWeek,
    DateFilterPastWeek,
    DateFilterPastMonth,
    DateFilterPastYear,
    DateFilterNextWeek,
    DateFilterNextMonth,
    DateFilterNextYear,
    ExistencePropertyFilter,
]
