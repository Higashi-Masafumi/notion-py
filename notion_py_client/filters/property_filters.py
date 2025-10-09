"""
プロパティフィルター統合型

各プロパティタイプに対応するフィルタークラス。
TypedDict を使用して公式 Notion API 仕様に準拠。

公式TypeScript定義:
type PropertyFilter =
  | { title: TextPropertyFilter; property: string; type?: "title" }
  | { rich_text: TextPropertyFilter; property: string; type?: "rich_text" }
  | { number: NumberPropertyFilter; property: string; type?: "number" }
  | { checkbox: CheckboxPropertyFilter; property: string; type?: "checkbox" }
  | { select: SelectPropertyFilter; property: string; type?: "select" }
  | { multi_select: MultiSelectPropertyFilter; property: string; type?: "multi_select" }
  | { status: StatusPropertyFilter; property: string; type?: "status" }
  | { date: DatePropertyFilter; property: string; type?: "date" }
  | { people: PeoplePropertyFilter; property: string; type?: "people" }
  | { files: ExistencePropertyFilter; property: string; type?: "files" }
  | { url: TextPropertyFilter; property: string; type?: "url" }
  | { email: TextPropertyFilter; property: string; type?: "email" }
  | { phone_number: TextPropertyFilter; property: string; type?: "phone_number" }
  | { relation: RelationPropertyFilter; property: string; type?: "relation" }
  | { created_by: PeoplePropertyFilter; property: string; type?: "created_by" }
  | { created_time: DatePropertyFilter; property: string; type?: "created_time" }
  | { last_edited_by: PeoplePropertyFilter; property: string; type?: "last_edited_by" }
  | { last_edited_time: DatePropertyFilter; property: string; type?: "last_edited_time" }
  | { formula: FormulaPropertyFilter; property: string; type?: "formula" }
  | { unique_id: NumberPropertyFilter; property: string; type?: "unique_id" }
  | { rollup: RollupPropertyFilter; property: string; type?: "rollup" }
  | { verification: VerificationPropertyStatusFilter; property: string; type?: "verification" }
"""

from typing import Literal, NotRequired, TypedDict, Union

from .advanced_filters import (
    FormulaPropertyFilter,
    RollupPropertyFilter,
    VerificationPropertyStatusFilter,
)
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
# Property Filter TypedDicts
# ============================================================================


class PropertyFilterTitle(TypedDict):
    """タイトルプロパティフィルター

    Examples:
        ```python
        filter: PropertyFilterTitle = {
            "property": "Name",
            "title": {"contains": "Important"}
        }
        ```
    """

    property: str
    title: TextPropertyFilter
    type: NotRequired[Literal["title"]]


class PropertyFilterRichText(TypedDict):
    """リッチテキストプロパティフィルター"""

    property: str
    rich_text: TextPropertyFilter
    type: NotRequired[Literal["rich_text"]]


class PropertyFilterNumber(TypedDict):
    """数値プロパティフィルター"""

    property: str
    number: NumberPropertyFilter
    type: NotRequired[Literal["number"]]


class PropertyFilterCheckbox(TypedDict):
    """チェックボックスプロパティフィルター"""

    property: str
    checkbox: CheckboxPropertyFilter
    type: NotRequired[Literal["checkbox"]]


class PropertyFilterSelect(TypedDict):
    """セレクトプロパティフィルター"""

    property: str
    select: SelectPropertyFilter
    type: NotRequired[Literal["select"]]


class PropertyFilterMultiSelect(TypedDict):
    """マルチセレクトプロパティフィルター"""

    property: str
    multi_select: MultiSelectPropertyFilter
    type: NotRequired[Literal["multi_select"]]


class PropertyFilterStatus(TypedDict):
    """ステータスプロパティフィルター"""

    property: str
    status: StatusPropertyFilter
    type: NotRequired[Literal["status"]]


class PropertyFilterDate(TypedDict):
    """日付プロパティフィルター"""

    property: str
    date: DatePropertyFilter
    type: NotRequired[Literal["date"]]


class PropertyFilterPeople(TypedDict):
    """Peopleプロパティフィルター"""

    property: str
    people: PeoplePropertyFilter
    type: NotRequired[Literal["people"]]


class PropertyFilterFiles(TypedDict):
    """ファイルプロパティフィルター"""

    property: str
    files: ExistencePropertyFilter
    type: NotRequired[Literal["files"]]


class PropertyFilterUrl(TypedDict):
    """URLプロパティフィルター"""

    property: str
    url: TextPropertyFilter
    type: NotRequired[Literal["url"]]


class PropertyFilterEmail(TypedDict):
    """メールプロパティフィルター"""

    property: str
    email: TextPropertyFilter
    type: NotRequired[Literal["email"]]


class PropertyFilterPhoneNumber(TypedDict):
    """電話番号プロパティフィルター"""

    property: str
    phone_number: TextPropertyFilter
    type: NotRequired[Literal["phone_number"]]


class PropertyFilterRelation(TypedDict):
    """Relationプロパティフィルター"""

    property: str
    relation: RelationPropertyFilter
    type: NotRequired[Literal["relation"]]


class PropertyFilterCreatedBy(TypedDict):
    """作成者プロパティフィルター"""

    property: str
    created_by: PeoplePropertyFilter
    type: NotRequired[Literal["created_by"]]


class PropertyFilterCreatedTime(TypedDict):
    """作成日時プロパティフィルター"""

    property: str
    created_time: DatePropertyFilter
    type: NotRequired[Literal["created_time"]]


class PropertyFilterLastEditedBy(TypedDict):
    """最終編集者プロパティフィルター"""

    property: str
    last_edited_by: PeoplePropertyFilter
    type: NotRequired[Literal["last_edited_by"]]


class PropertyFilterLastEditedTime(TypedDict):
    """最終編集日時プロパティフィルター"""

    property: str
    last_edited_time: DatePropertyFilter
    type: NotRequired[Literal["last_edited_time"]]


class PropertyFilterFormula(TypedDict):
    """Formulaプロパティフィルター"""

    property: str
    formula: FormulaPropertyFilter
    type: NotRequired[Literal["formula"]]


class PropertyFilterUniqueId(TypedDict):
    """ユニークIDプロパティフィルター"""

    property: str
    unique_id: NumberPropertyFilter
    type: NotRequired[Literal["unique_id"]]


class PropertyFilterRollup(TypedDict):
    """Rollupプロパティフィルター"""

    property: str
    rollup: RollupPropertyFilter
    type: NotRequired[Literal["rollup"]]


class PropertyFilterVerification(TypedDict):
    """検証プロパティフィルター"""

    property: str
    verification: VerificationPropertyStatusFilter
    type: NotRequired[Literal["verification"]]


# ============================================================================
# Property Filter Union Type
# ============================================================================

# Matches TypeScript: type PropertyFilter = ...
PropertyFilter = Union[
    PropertyFilterTitle,
    PropertyFilterRichText,
    PropertyFilterNumber,
    PropertyFilterCheckbox,
    PropertyFilterSelect,
    PropertyFilterMultiSelect,
    PropertyFilterStatus,
    PropertyFilterDate,
    PropertyFilterPeople,
    PropertyFilterFiles,
    PropertyFilterUrl,
    PropertyFilterEmail,
    PropertyFilterPhoneNumber,
    PropertyFilterRelation,
    PropertyFilterCreatedBy,
    PropertyFilterCreatedTime,
    PropertyFilterLastEditedBy,
    PropertyFilterLastEditedTime,
    PropertyFilterFormula,
    PropertyFilterUniqueId,
    PropertyFilterRollup,
    PropertyFilterVerification,
]
