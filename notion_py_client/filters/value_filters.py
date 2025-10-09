"""
値フィルター定義

テキスト、数値、選択肢等の値に対するフィルター条件。
TypedDict を使用して公式 Notion API 仕様に準拠。

公式TypeScript定義:
- type TextPropertyFilter = { equals: string } | { does_not_equal: string } | ...
- type NumberPropertyFilter = { equals: number } | { does_not_equal: number } | ...
- type CheckboxPropertyFilter = { equals: boolean } | { does_not_equal: boolean }
"""

from typing import TypedDict, Union

from .base_filters import ExistencePropertyFilter


# ============================================================================
# Text Property Filters
# ============================================================================


class TextFilterEquals(TypedDict):
    """テキストが等しい

    Examples:
        ```python
        filter: TextFilterEquals = {"equals": "Important"}
        ```
    """

    equals: str


class TextFilterDoesNotEqual(TypedDict):
    """テキストが等しくない"""

    does_not_equal: str


class TextFilterContains(TypedDict):
    """テキストを含む"""

    contains: str


class TextFilterDoesNotContain(TypedDict):
    """テキストを含まない"""

    does_not_contain: str


class TextFilterStartsWith(TypedDict):
    """テキストで始まる"""

    starts_with: str


class TextFilterEndsWith(TypedDict):
    """テキストで終わる"""

    ends_with: str


# Matches TypeScript: type TextPropertyFilter = { equals: string } | ... | ExistencePropertyFilter
TextPropertyFilter = Union[
    TextFilterEquals,
    TextFilterDoesNotEqual,
    TextFilterContains,
    TextFilterDoesNotContain,
    TextFilterStartsWith,
    TextFilterEndsWith,
    ExistencePropertyFilter,
]


# ============================================================================
# Number Property Filters
# ============================================================================


class NumberFilterEquals(TypedDict):
    """数値が等しい

    Examples:
        ```python
        filter: NumberFilterEquals = {"equals": 100}
        ```
    """

    equals: float


class NumberFilterDoesNotEqual(TypedDict):
    """数値が等しくない"""

    does_not_equal: float


class NumberFilterGreaterThan(TypedDict):
    """数値がより大きい"""

    greater_than: float


class NumberFilterLessThan(TypedDict):
    """数値がより小さい"""

    less_than: float


class NumberFilterGreaterThanOrEqualTo(TypedDict):
    """数値が以上"""

    greater_than_or_equal_to: float


class NumberFilterLessThanOrEqualTo(TypedDict):
    """数値が以下"""

    less_than_or_equal_to: float


# Matches TypeScript: type NumberPropertyFilter = { equals: number } | ... | ExistencePropertyFilter
NumberPropertyFilter = Union[
    NumberFilterEquals,
    NumberFilterDoesNotEqual,
    NumberFilterGreaterThan,
    NumberFilterLessThan,
    NumberFilterGreaterThanOrEqualTo,
    NumberFilterLessThanOrEqualTo,
    ExistencePropertyFilter,
]


# ============================================================================
# Checkbox Property Filters
# ============================================================================


class CheckboxFilterEquals(TypedDict):
    """チェックボックスが等しい

    Examples:
        ```python
        filter: CheckboxFilterEquals = {"equals": True}
        ```
    """

    equals: bool


class CheckboxFilterDoesNotEqual(TypedDict):
    """チェックボックスが等しくない"""

    does_not_equal: bool


# Matches TypeScript: type CheckboxPropertyFilter = { equals: boolean } | { does_not_equal: boolean }
CheckboxPropertyFilter = Union[CheckboxFilterEquals, CheckboxFilterDoesNotEqual]


# ============================================================================
# Select Property Filters
# ============================================================================


class SelectFilterEquals(TypedDict):
    """選択肢が等しい

    Examples:
        ```python
        filter: SelectFilterEquals = {"equals": "Option A"}
        ```
    """

    equals: str


class SelectFilterDoesNotEqual(TypedDict):
    """選択肢が等しくない"""

    does_not_equal: str


# Matches TypeScript: type SelectPropertyFilter = { equals: string } | { does_not_equal: string } | ExistencePropertyFilter
SelectPropertyFilter = Union[
    SelectFilterEquals,
    SelectFilterDoesNotEqual,
    ExistencePropertyFilter,
]


# ============================================================================
# Multi-Select Property Filters
# ============================================================================


class MultiSelectFilterContains(TypedDict):
    """マルチセレクトが含む

    Examples:
        ```python
        filter: MultiSelectFilterContains = {"contains": "Tag A"}
        ```
    """

    contains: str


class MultiSelectFilterDoesNotContain(TypedDict):
    """マルチセレクトが含まない"""

    does_not_contain: str


# Matches TypeScript: type MultiSelectPropertyFilter = { contains: string } | { does_not_contain: string } | ExistencePropertyFilter
MultiSelectPropertyFilter = Union[
    MultiSelectFilterContains,
    MultiSelectFilterDoesNotContain,
    ExistencePropertyFilter,
]


# ============================================================================
# Status Property Filters
# ============================================================================


class StatusFilterEquals(TypedDict):
    """ステータスが等しい

    Examples:
        ```python
        filter: StatusFilterEquals = {"equals": "In Progress"}
        ```
    """

    equals: str


class StatusFilterDoesNotEqual(TypedDict):
    """ステータスが等しくない"""

    does_not_equal: str


# Matches TypeScript: type StatusPropertyFilter = { equals: string } | { does_not_equal: string } | ExistencePropertyFilter
StatusPropertyFilter = Union[
    StatusFilterEquals,
    StatusFilterDoesNotEqual,
    ExistencePropertyFilter,
]
