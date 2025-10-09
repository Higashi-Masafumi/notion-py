"""
高度なフィルター定義

Formula、Rollup、Verificationフィルター条件。
TypedDict を使用して公式 Notion API 仕様に準拠。

公式TypeScript定義:
type FormulaPropertyFilter =
  | { string: TextPropertyFilter }
  | { checkbox: CheckboxPropertyFilter }
  | { number: NumberPropertyFilter }
  | { date: DatePropertyFilter }

type RollupSubfilterPropertyFilter =
  | { rich_text: TextPropertyFilter }
  | { number: NumberPropertyFilter }
  | { checkbox: CheckboxPropertyFilter }
  | { select: SelectPropertyFilter }
  | { multi_select: MultiSelectPropertyFilter }
  | { relation: RelationPropertyFilter }
  | { date: DatePropertyFilter }
  | { people: PeoplePropertyFilter }
  | { files: ExistencePropertyFilter }
  | { status: StatusPropertyFilter }

type RollupPropertyFilter =
  | { any: RollupSubfilterPropertyFilter }
  | { none: RollupSubfilterPropertyFilter }
  | { every: RollupSubfilterPropertyFilter }
  | { date: DatePropertyFilter }
  | { number: NumberPropertyFilter }

type VerificationPropertyStatusFilter = {
  status: "verified" | "expired" | "none"
}
"""

from typing import Literal, TypedDict, Union

from .base_filters import ExistencePropertyFilter
from .date_filters import DatePropertyFilter
from .relation_filters import PeoplePropertyFilter, RelationPropertyFilter
from .value_filters import (
    CheckboxPropertyFilter,
    MultiSelectPropertyFilter,
    NumberPropertyFilter,
    SelectPropertyFilter,
    StatusPropertyFilter,
    TextPropertyFilter,
)


# ============================================================================
# Formula Property Filters
# ============================================================================


class FormulaFilterString(TypedDict):
    """Formula文字列フィルター

    Examples:
        ```python
        filter: FormulaFilterString = {
            "string": {"contains": "test"}
        }
        ```
    """

    string: TextPropertyFilter


class FormulaFilterCheckbox(TypedDict):
    """Formulaチェックボックスフィルター"""

    checkbox: CheckboxPropertyFilter


class FormulaFilterNumber(TypedDict):
    """Formula数値フィルター"""

    number: NumberPropertyFilter


class FormulaFilterDate(TypedDict):
    """Formula日付フィルター"""

    date: DatePropertyFilter


# Matches TypeScript: type FormulaPropertyFilter
FormulaPropertyFilter = Union[
    FormulaFilterString,
    FormulaFilterCheckbox,
    FormulaFilterNumber,
    FormulaFilterDate,
]


# ============================================================================
# Rollup Subfilter Property Filters
# ============================================================================


class RollupSubfilterRichText(TypedDict):
    """Rollupリッチテキストフィルター"""

    rich_text: TextPropertyFilter


class RollupSubfilterNumber(TypedDict):
    """Rollup数値フィルター"""

    number: NumberPropertyFilter


class RollupSubfilterCheckbox(TypedDict):
    """Rollupチェックボックスフィルター"""

    checkbox: CheckboxPropertyFilter


class RollupSubfilterSelect(TypedDict):
    """Rollupセレクトフィルター"""

    select: SelectPropertyFilter


class RollupSubfilterMultiSelect(TypedDict):
    """Rollupマルチセレクトフィルター"""

    multi_select: MultiSelectPropertyFilter


class RollupSubfilterRelation(TypedDict):
    """Rollup Relationフィルター"""

    relation: RelationPropertyFilter


class RollupSubfilterDate(TypedDict):
    """Rollup日付フィルター"""

    date: DatePropertyFilter


class RollupSubfilterPeople(TypedDict):
    """Rollup Peopleフィルター"""

    people: PeoplePropertyFilter


class RollupSubfilterFiles(TypedDict):
    """Rollupファイルフィルター"""

    files: ExistencePropertyFilter


class RollupSubfilterStatus(TypedDict):
    """Rollupステータスフィルター"""

    status: StatusPropertyFilter


# Matches TypeScript: type RollupSubfilterPropertyFilter
RollupSubfilterPropertyFilter = Union[
    RollupSubfilterRichText,
    RollupSubfilterNumber,
    RollupSubfilterCheckbox,
    RollupSubfilterSelect,
    RollupSubfilterMultiSelect,
    RollupSubfilterRelation,
    RollupSubfilterDate,
    RollupSubfilterPeople,
    RollupSubfilterFiles,
    RollupSubfilterStatus,
]


# ============================================================================
# Rollup Property Filters
# ============================================================================


class RollupFilterAny(TypedDict):
    """Rollup いずれかが一致

    Examples:
        ```python
        filter: RollupFilterAny = {
            "any": {"number": {"greater_than": 100}}
        }
        ```
    """

    any: RollupSubfilterPropertyFilter


class RollupFilterNone(TypedDict):
    """Rollup いずれも一致しない"""

    none: RollupSubfilterPropertyFilter


class RollupFilterEvery(TypedDict):
    """Rollup すべてが一致"""

    every: RollupSubfilterPropertyFilter


class RollupFilterDate(TypedDict):
    """Rollup日付フィルター"""

    date: DatePropertyFilter


class RollupFilterNumber(TypedDict):
    """Rollup数値フィルター"""

    number: NumberPropertyFilter


# Matches TypeScript: type RollupPropertyFilter
RollupPropertyFilter = Union[
    RollupFilterAny,
    RollupFilterNone,
    RollupFilterEvery,
    RollupFilterDate,
    RollupFilterNumber,
]


# ============================================================================
# Verification Property Status Filter
# ============================================================================


class VerificationPropertyStatusFilter(TypedDict):
    """検証ステータスフィルター

    Examples:
        ```python
        filter: VerificationPropertyStatusFilter = {"status": "verified"}
        ```
    """

    status: Literal["verified", "expired", "none"]
