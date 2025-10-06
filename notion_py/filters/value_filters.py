"""
値フィルター定義

テキスト、数値、チェックボックス、セレクト系のフィルター条件。
"""

from typing import Union

from pydantic import BaseModel, Field, StrictBool, StrictStr

from .base_filters import ExistenceFilterEmpty, ExistenceFilterNotEmpty


# ===== テキストフィルター =====


class TextFilterEquals(BaseModel):
    """テキストが等しい"""

    equals: StrictStr = Field(..., description="一致する文字列")


class TextFilterDoesNotEqual(BaseModel):
    """テキストが等しくない"""

    does_not_equal: StrictStr = Field(..., description="一致しない文字列")


class TextFilterContains(BaseModel):
    """テキストを含む"""

    contains: StrictStr = Field(..., description="含む文字列")


class TextFilterDoesNotContain(BaseModel):
    """テキストを含まない"""

    does_not_contain: StrictStr = Field(..., description="含まない文字列")


class TextFilterStartsWith(BaseModel):
    """テキストで始まる"""

    starts_with: StrictStr = Field(..., description="開始文字列")


class TextFilterEndsWith(BaseModel):
    """テキストで終わる"""

    ends_with: StrictStr = Field(..., description="終了文字列")


TextPropertyFilter = Union[
    TextFilterEquals,
    TextFilterDoesNotEqual,
    TextFilterContains,
    TextFilterDoesNotContain,
    TextFilterStartsWith,
    TextFilterEndsWith,
    ExistenceFilterEmpty,
    ExistenceFilterNotEmpty,
]


# ===== 数値フィルター =====


class NumberFilterEquals(BaseModel):
    """数値が等しい"""

    equals: int | float = Field(..., description="一致する数値")


class NumberFilterDoesNotEqual(BaseModel):
    """数値が等しくない"""

    does_not_equal: int | float = Field(..., description="一致しない数値")


class NumberFilterGreaterThan(BaseModel):
    """数値より大きい"""

    greater_than: int | float = Field(..., description="比較する数値")


class NumberFilterLessThan(BaseModel):
    """数値より小さい"""

    less_than: int | float = Field(..., description="比較する数値")


class NumberFilterGreaterThanOrEqualTo(BaseModel):
    """数値以上"""

    greater_than_or_equal_to: int | float = Field(..., description="比較する数値")


class NumberFilterLessThanOrEqualTo(BaseModel):
    """数値以下"""

    less_than_or_equal_to: int | float = Field(..., description="比較する数値")


NumberPropertyFilter = Union[
    NumberFilterEquals,
    NumberFilterDoesNotEqual,
    NumberFilterGreaterThan,
    NumberFilterLessThan,
    NumberFilterGreaterThanOrEqualTo,
    NumberFilterLessThanOrEqualTo,
    ExistenceFilterEmpty,
    ExistenceFilterNotEmpty,
]


# ===== チェックボックスフィルター =====


class CheckboxFilterEquals(BaseModel):
    """チェックボックスが等しい"""

    equals: StrictBool = Field(..., description="一致する真偽値")


class CheckboxFilterDoesNotEqual(BaseModel):
    """チェックボックスが等しくない"""

    does_not_equal: StrictBool = Field(..., description="一致しない真偽値")


CheckboxPropertyFilter = Union[
    CheckboxFilterEquals,
    CheckboxFilterDoesNotEqual,
]


# ===== セレクトフィルター =====


class SelectFilterEquals(BaseModel):
    """セレクトが等しい"""

    equals: StrictStr = Field(..., description="一致する選択肢")


class SelectFilterDoesNotEqual(BaseModel):
    """セレクトが等しくない"""

    does_not_equal: StrictStr = Field(..., description="一致しない選択肢")


SelectPropertyFilter = Union[
    SelectFilterEquals,
    SelectFilterDoesNotEqual,
    ExistenceFilterEmpty,
    ExistenceFilterNotEmpty,
]


# ===== マルチセレクトフィルター =====


class MultiSelectFilterContains(BaseModel):
    """マルチセレクトが含む"""

    contains: StrictStr = Field(..., description="含む選択肢")


class MultiSelectFilterDoesNotContain(BaseModel):
    """マルチセレクトが含まない"""

    does_not_contain: StrictStr = Field(..., description="含まない選択肢")


MultiSelectPropertyFilter = Union[
    MultiSelectFilterContains,
    MultiSelectFilterDoesNotContain,
    ExistenceFilterEmpty,
    ExistenceFilterNotEmpty,
]


# ===== ステータスフィルター =====


class StatusFilterEquals(BaseModel):
    """ステータスが等しい"""

    equals: StrictStr = Field(..., description="一致するステータス")


class StatusFilterDoesNotEqual(BaseModel):
    """ステータスが等しくない"""

    does_not_equal: StrictStr = Field(..., description="一致しないステータス")


StatusPropertyFilter = Union[
    StatusFilterEquals,
    StatusFilterDoesNotEqual,
    ExistenceFilterEmpty,
    ExistenceFilterNotEmpty,
]
