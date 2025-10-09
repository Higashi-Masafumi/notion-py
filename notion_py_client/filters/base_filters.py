"""
基本的なフィルター定義

存在性チェック等の基本的なフィルター条件。
TypedDict を使用して公式 Notion API 仕様に準拠。
"""

from typing import Literal, TypedDict, Union


class ExistenceFilterEmpty(TypedDict):
    """空であることをチェック

    Examples:
        ```python
        filter: ExistenceFilterEmpty = {"is_empty": True}
        ```
    """

    is_empty: Literal[True]


class ExistenceFilterNotEmpty(TypedDict):
    """空でないことをチェック

    Examples:
        ```python
        filter: ExistenceFilterNotEmpty = {"is_not_empty": True}
        ```
    """

    is_not_empty: Literal[True]


# Union type for existence filters
# Matches TypeScript: type ExistencePropertyFilter = { is_empty: true } | { is_not_empty: true }
ExistencePropertyFilter = Union[ExistenceFilterEmpty, ExistenceFilterNotEmpty]
