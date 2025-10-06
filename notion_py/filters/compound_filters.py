"""
複合フィルター定義

AND/ORなどの複合条件フィルター。
公式TypeScript SDKのGroupFilterOperatorArray型に対応。
"""

from typing import Union

from pydantic import BaseModel, Field

from .property_filters import PropertyFilter
from .timestamp_filters import TimestampFilter


# 公式SDK: PropertyOrTimestampFilter = PropertyFilter | TimestampFilter
PropertyOrTimestampFilter = Union[PropertyFilter, TimestampFilter]


class AndFilter(BaseModel):
    """
    ANDフィルター (公式SDK: { and: PropertyOrTimestampFilterArray })

    複数の条件をすべて満たすレコードを抽出する。

    Examples:
        ```python
        # ステータスが"Active" かつ 金額が10000より大きい
        filter_obj = AndFilter(
            **{
                "and": [
                    PropertyFilterStatus(...),
                    PropertyFilterNumber(...),
                ]
            }
        )
        ```
    """

    and_: list["FilterCondition"] = Field(
        ..., alias="and", description="AND条件のリスト (すべて満たす必要がある)"
    )


class OrFilter(BaseModel):
    """
    ORフィルター (公式SDK: { or: PropertyOrTimestampFilterArray })

    複数の条件のいずれかを満たすレコードを抽出する。

    Examples:
        ```python
        # サービスが"A" または "B"
        filter_obj = OrFilter(
            **{
                "or": [
                    PropertyFilterSelect(...),
                    PropertyFilterSelect(...),
                ]
            }
        )
        ```
    """

    or_: list["FilterCondition"] = Field(
        ..., alias="or", description="OR条件のリスト (いずれかを満たせばよい)"
    )


# 公式SDK: GroupFilterOperatorArray = Array<PropertyOrTimestampFilter | { and: ... } | { or: ... }>
FilterCondition = Union[
    PropertyOrTimestampFilter,
    AndFilter,
    OrFilter,
]

# 前方参照を解決 (Pydantic v2)
AndFilter.model_rebuild()
OrFilter.model_rebuild()
