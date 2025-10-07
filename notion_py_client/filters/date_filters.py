"""
日付フィルター定義

日付プロパティに対するフィルター条件。
"""

from typing import Union

from pydantic import BaseModel, Field, StrictStr

from .base_filters import ExistenceFilterEmpty, ExistenceFilterNotEmpty


class DateFilterEquals(BaseModel):
    """日付が等しい"""

    equals: StrictStr = Field(..., description="一致する日付(ISO 8601)")


class DateFilterBefore(BaseModel):
    """日付より前"""

    before: StrictStr = Field(..., description="基準日付(ISO 8601)")


class DateFilterAfter(BaseModel):
    """日付より後"""

    after: StrictStr = Field(..., description="基準日付(ISO 8601)")


class DateFilterOnOrBefore(BaseModel):
    """日付以前"""

    on_or_before: StrictStr = Field(..., description="基準日付(ISO 8601)")


class DateFilterOnOrAfter(BaseModel):
    """日付以降"""

    on_or_after: StrictStr = Field(..., description="基準日付(ISO 8601)")


class DateFilterThisWeek(BaseModel):
    """今週"""

    this_week: dict = Field(default_factory=dict, description="今週")


class DateFilterPastWeek(BaseModel):
    """先週"""

    past_week: dict = Field(default_factory=dict, description="先週")


class DateFilterPastMonth(BaseModel):
    """先月"""

    past_month: dict = Field(default_factory=dict, description="先月")


class DateFilterPastYear(BaseModel):
    """昨年"""

    past_year: dict = Field(default_factory=dict, description="昨年")


class DateFilterNextWeek(BaseModel):
    """来週"""

    next_week: dict = Field(default_factory=dict, description="来週")


class DateFilterNextMonth(BaseModel):
    """来月"""

    next_month: dict = Field(default_factory=dict, description="来月")


class DateFilterNextYear(BaseModel):
    """来年"""

    next_year: dict = Field(default_factory=dict, description="来年")


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
    ExistenceFilterEmpty,
    ExistenceFilterNotEmpty,
]
