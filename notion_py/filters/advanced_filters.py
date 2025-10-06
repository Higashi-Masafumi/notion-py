"""
高度なフィルター定義

Formula、Rollup、Verificationフィルター条件。
"""

from typing import Literal, Union

from pydantic import BaseModel, Field

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


# ===== Formulaフィルター =====


class FormulaFilterString(BaseModel):
    """Formula文字列フィルター"""

    string: TextPropertyFilter = Field(..., description="文字列フィルター")


class FormulaFilterCheckbox(BaseModel):
    """Formulaチェックボックスフィルター"""

    checkbox: CheckboxPropertyFilter = Field(
        ..., description="チェックボックスフィルター"
    )


class FormulaFilterNumber(BaseModel):
    """Formula数値フィルター"""

    number: NumberPropertyFilter = Field(..., description="数値フィルター")


class FormulaFilterDate(BaseModel):
    """Formula日付フィルター"""

    date: DatePropertyFilter = Field(..., description="日付フィルター")


FormulaPropertyFilter = Union[
    FormulaFilterString,
    FormulaFilterCheckbox,
    FormulaFilterNumber,
    FormulaFilterDate,
]


# ===== Rollupサブフィルター =====


class RollupSubfilterRichText(BaseModel):
    """Rollupリッチテキストフィルター"""

    rich_text: TextPropertyFilter = Field(..., description="リッチテキストフィルター")


class RollupSubfilterNumber(BaseModel):
    """Rollup数値フィルター"""

    number: NumberPropertyFilter = Field(..., description="数値フィルター")


class RollupSubfilterCheckbox(BaseModel):
    """Rollupチェックボックスフィルター"""

    checkbox: CheckboxPropertyFilter = Field(
        ..., description="チェックボックスフィルター"
    )


class RollupSubfilterSelect(BaseModel):
    """Rollupセレクトフィルター"""

    select: SelectPropertyFilter = Field(..., description="セレクトフィルター")


class RollupSubfilterMultiSelect(BaseModel):
    """Rollupマルチセレクトフィルター"""

    multi_select: MultiSelectPropertyFilter = Field(
        ..., description="マルチセレクトフィルター"
    )


class RollupSubfilterRelation(BaseModel):
    """Rollup Relationフィルター"""

    relation: RelationPropertyFilter = Field(..., description="Relationフィルター")


class RollupSubfilterDate(BaseModel):
    """Rollup日付フィルター"""

    date: DatePropertyFilter = Field(..., description="日付フィルター")


class RollupSubfilterPeople(BaseModel):
    """Rollup Peopleフィルター"""

    people: PeoplePropertyFilter = Field(..., description="Peopleフィルター")


class RollupSubfilterFiles(BaseModel):
    """Rollupファイルフィルター"""

    files: ExistencePropertyFilter = Field(..., description="ファイル存在性フィルター")


class RollupSubfilterStatus(BaseModel):
    """Rollupステータスフィルター"""

    status: StatusPropertyFilter = Field(..., description="ステータスフィルター")


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


# ===== Rollupフィルター =====


class RollupFilterAny(BaseModel):
    """Rollup いずれかが一致"""

    any: RollupSubfilterPropertyFilter = Field(
        ..., description="いずれかが一致する条件"
    )


class RollupFilterNone(BaseModel):
    """Rollup いずれも一致しない"""

    none: RollupSubfilterPropertyFilter = Field(
        ..., description="いずれも一致しない条件"
    )


class RollupFilterEvery(BaseModel):
    """Rollup すべてが一致"""

    every: RollupSubfilterPropertyFilter = Field(
        ..., description="すべてが一致する条件"
    )


class RollupFilterDate(BaseModel):
    """Rollup日付フィルター"""

    date: DatePropertyFilter = Field(..., description="日付フィルター")


class RollupFilterNumber(BaseModel):
    """Rollup数値フィルター"""

    number: NumberPropertyFilter = Field(..., description="数値フィルター")


RollupPropertyFilter = Union[
    RollupFilterAny,
    RollupFilterNone,
    RollupFilterEvery,
    RollupFilterDate,
    RollupFilterNumber,
]


# ===== Verificationフィルター =====


class VerificationPropertyStatusFilter(BaseModel):
    """検証ステータスフィルター"""

    status: Literal["verified", "expired", "none"] = Field(
        ..., description="検証ステータス"
    )
