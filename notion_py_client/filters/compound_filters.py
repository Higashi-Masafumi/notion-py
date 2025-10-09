"""
複合フィルター定義

AND/ORなどの複合条件フィルター。
TypedDict を使用して公式 Notion API 仕様に準拠。

公式TypeScript定義:
type PropertyOrTimestampFilter = PropertyFilter | TimestampFilter
type PropertyOrTimestampFilterArray = Array<PropertyOrTimestampFilter>
type GroupFilterOperatorArray = Array<
  | PropertyOrTimestampFilter
  | { or: PropertyOrTimestampFilterArray }
  | { and: PropertyOrTimestampFilterArray }
>
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from typing import TypedDict

    from .property_filters import PropertyFilter
    from .timestamp_filters import TimestampFilter

    # TYPE_CHECKING時のみ使用: 正確な型定義
    PropertyOrTimestampFilter = Union[PropertyFilter, TimestampFilter]

    class AndFilterDict(TypedDict):
        """ANDフィルター (型チェック用)"""

        and_: list[Union[PropertyOrTimestampFilter, "AndFilterDict", "OrFilterDict"]]  # type: ignore

    class OrFilterDict(TypedDict):
        """ORフィルター (型チェック用)"""

        or_: list[Union[PropertyOrTimestampFilter, "AndFilterDict", "OrFilterDict"]]  # type: ignore

    # 完全な FilterCondition 型定義
    FilterCondition = Union[
        PropertyFilter,
        TimestampFilter,
        AndFilterDict,
        OrFilterDict,
    ]
else:
    # 実行時: 循環参照を避けるため dict を使用
    AndFilterDict = dict[str, list[Any]]  # {"and": [...]}
    OrFilterDict = dict[str, list[Any]]  # {"or": [...]}
    FilterCondition = dict[str, Any]


# ============================================================================
# Helper Functions for Type-Safe Filter Construction
# ============================================================================

if TYPE_CHECKING:
    # 型チェック時: 正確な型シグネチャ
    def create_and_filter(
        *conditions: Union[PropertyFilter, TimestampFilter, AndFilterDict, OrFilterDict]
    ) -> AndFilterDict: ...

    def create_or_filter(
        *conditions: Union[PropertyFilter, TimestampFilter, AndFilterDict, OrFilterDict]
    ) -> OrFilterDict: ...

else:
    # 実行時: 実装
    def create_and_filter(*conditions: dict[str, Any]) -> AndFilterDict:
        """AND フィルターを作成するヘルパー関数

        すべての条件を満たすレコードを抽出する。

        Examples:
            ```python
            from notion_py_client.filters import create_and_filter

            filter = create_and_filter(
                {"property": "Status", "status": {"equals": "Active"}},
                {"property": "Amount", "number": {"greater_than": 10000}},
            )
            # => {"and": [{...}, {...}]}
            ```

        Args:
            *conditions: フィルター条件（PropertyFilter, TimestampFilter, または入れ子の複合フィルター）

        Returns:
            ANDフィルター辞書 `{"and": [...]}`
        """
        return {"and": list(conditions)}

    def create_or_filter(*conditions: dict[str, Any]) -> OrFilterDict:
        """OR フィルターを作成するヘルパー関数

        いずれかの条件を満たすレコードを抽出する。

        Examples:
            ```python
            from notion_py_client.filters import create_or_filter

            filter = create_or_filter(
                {"property": "Service", "select": {"equals": "A"}},
                {"property": "Service", "select": {"equals": "B"}},
            )
            # => {"or": [{...}, {...}]}
            ```

        Args:
            *conditions: フィルター条件（PropertyFilter, TimestampFilter, または入れ子の複合フィルター）

        Returns:
            ORフィルター辞書 `{"or": [...]}`
        """
        return {"or": list(conditions)}
