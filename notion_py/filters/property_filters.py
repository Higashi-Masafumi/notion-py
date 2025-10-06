"""
プロパティフィルター統合型

各プロパティタイプに対応するフィルタークラス。
公式TypeScript SDKのPropertyFilter型に対応。
"""

from typing import Literal, Union

from pydantic import BaseModel, Field

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


class PropertyFilterTitle(BaseModel):
    """タイトルプロパティフィルター (title: TextPropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    title: TextPropertyFilter = Field(..., description="タイトルフィルター条件")
    type: Literal["title"] = Field(default="title", description="プロパティタイプ")


class PropertyFilterRichText(BaseModel):
    """リッチテキストプロパティフィルター (rich_text: TextPropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    rich_text: TextPropertyFilter = Field(
        ..., description="リッチテキストフィルター条件"
    )
    type: Literal["rich_text"] = Field(
        default="rich_text", description="プロパティタイプ"
    )


class PropertyFilterNumber(BaseModel):
    """数値プロパティフィルター (number: NumberPropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    number: NumberPropertyFilter = Field(..., description="数値フィルター条件")
    type: Literal["number"] = Field(default="number", description="プロパティタイプ")


class PropertyFilterCheckbox(BaseModel):
    """チェックボックスプロパティフィルター (checkbox: CheckboxPropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    checkbox: CheckboxPropertyFilter = Field(
        ..., description="チェックボックスフィルター条件"
    )
    type: Literal["checkbox"] = Field(
        default="checkbox", description="プロパティタイプ"
    )


class PropertyFilterSelect(BaseModel):
    """セレクトプロパティフィルター (select: SelectPropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    select: SelectPropertyFilter = Field(..., description="セレクトフィルター条件")
    type: Literal["select"] = Field(default="select", description="プロパティタイプ")


class PropertyFilterMultiSelect(BaseModel):
    """マルチセレクトプロパティフィルター (multi_select: MultiSelectPropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    multi_select: MultiSelectPropertyFilter = Field(
        ..., description="マルチセレクトフィルター条件"
    )
    type: Literal["multi_select"] = Field(
        default="multi_select", description="プロパティタイプ"
    )


class PropertyFilterStatus(BaseModel):
    """ステータスプロパティフィルター (status: StatusPropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    status: StatusPropertyFilter = Field(..., description="ステータスフィルター条件")
    type: Literal["status"] = Field(default="status", description="プロパティタイプ")


class PropertyFilterDate(BaseModel):
    """日付プロパティフィルター (date: DatePropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    date: DatePropertyFilter = Field(..., description="日付フィルター条件")
    type: Literal["date"] = Field(default="date", description="プロパティタイプ")


class PropertyFilterPeople(BaseModel):
    """Peopleプロパティフィルター (people: PeoplePropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    people: PeoplePropertyFilter = Field(..., description="Peopleフィルター条件")
    type: Literal["people"] = Field(default="people", description="プロパティタイプ")


class PropertyFilterFiles(BaseModel):
    """ファイルプロパティフィルター (files: ExistencePropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    files: ExistencePropertyFilter = Field(..., description="ファイルフィルター条件")
    type: Literal["files"] = Field(default="files", description="プロパティタイプ")


class PropertyFilterUrl(BaseModel):
    """URLプロパティフィルター (url: TextPropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    url: TextPropertyFilter = Field(..., description="URLフィルター条件")
    type: Literal["url"] = Field(default="url", description="プロパティタイプ")


class PropertyFilterEmail(BaseModel):
    """メールプロパティフィルター (email: TextPropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    email: TextPropertyFilter = Field(..., description="メールフィルター条件")
    type: Literal["email"] = Field(default="email", description="プロパティタイプ")


class PropertyFilterPhoneNumber(BaseModel):
    """電話番号プロパティフィルター (phone_number: TextPropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    phone_number: TextPropertyFilter = Field(..., description="電話番号フィルター条件")
    type: Literal["phone_number"] = Field(
        default="phone_number", description="プロパティタイプ"
    )


class PropertyFilterRelation(BaseModel):
    """Relationプロパティフィルター (relation: RelationPropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    relation: RelationPropertyFilter = Field(..., description="Relationフィルター条件")
    type: Literal["relation"] = Field(
        default="relation", description="プロパティタイプ"
    )


class PropertyFilterCreatedBy(BaseModel):
    """作成者プロパティフィルター (created_by: PeoplePropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    created_by: PeoplePropertyFilter = Field(..., description="作成者フィルター条件")
    type: Literal["created_by"] = Field(
        default="created_by", description="プロパティタイプ"
    )


class PropertyFilterCreatedTime(BaseModel):
    """作成日時プロパティフィルター (created_time: DatePropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    created_time: DatePropertyFilter = Field(..., description="作成日時フィルター条件")
    type: Literal["created_time"] = Field(
        default="created_time", description="プロパティタイプ"
    )


class PropertyFilterLastEditedBy(BaseModel):
    """最終編集者プロパティフィルター (last_edited_by: PeoplePropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    last_edited_by: PeoplePropertyFilter = Field(
        ..., description="最終編集者フィルター条件"
    )
    type: Literal["last_edited_by"] = Field(
        default="last_edited_by", description="プロパティタイプ"
    )


class PropertyFilterLastEditedTime(BaseModel):
    """最終編集日時プロパティフィルター (last_edited_time: DatePropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    last_edited_time: DatePropertyFilter = Field(
        ..., description="最終編集日時フィルター条件"
    )
    type: Literal["last_edited_time"] = Field(
        default="last_edited_time", description="プロパティタイプ"
    )


class PropertyFilterFormula(BaseModel):
    """Formulaプロパティフィルター (formula: FormulaPropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    formula: FormulaPropertyFilter = Field(..., description="Formulaフィルター条件")
    type: Literal["formula"] = Field(default="formula", description="プロパティタイプ")


class PropertyFilterUniqueId(BaseModel):
    """ユニークIDプロパティフィルター (unique_id: NumberPropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    unique_id: NumberPropertyFilter = Field(..., description="ユニークIDフィルター条件")
    type: Literal["unique_id"] = Field(
        default="unique_id", description="プロパティタイプ"
    )


class PropertyFilterRollup(BaseModel):
    """Rollupプロパティフィルター (rollup: RollupPropertyFilter)"""

    property: str = Field(..., description="プロパティ名")
    rollup: RollupPropertyFilter = Field(..., description="Rollupフィルター条件")
    type: Literal["rollup"] = Field(default="rollup", description="プロパティタイプ")


class PropertyFilterVerification(BaseModel):
    """検証プロパティフィルター (verification: VerificationPropertyStatusFilter)"""

    property: str = Field(..., description="プロパティ名")
    verification: VerificationPropertyStatusFilter = Field(
        ..., description="検証フィルター条件"
    )
    type: Literal["verification"] = Field(
        default="verification", description="プロパティタイプ"
    )


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
