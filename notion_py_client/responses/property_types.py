"""
プロパティ型の定義

PageObjectResponseで使用されるプロパティ値の型定義。
"""

from typing import Union

from ..properties import RelationProperty, RollupProperty
from ..properties.base_properties import (
    ButtonProperty,
    CheckboxProperty,
    CreatedByProperty,
    CreatedTimeProperty,
    DateProperty,
    EmailProperty,
    FormulaProperty,
    FilesProperty,
    LastEditedByProperty,
    MultiSelectProperty,
    NumberProperty,
    PeopleProperty,
    PhoneNumberProperty,
    RichTextProperty,
    SelectProperty,
    StatusProperty,
    TitleProperty,
    UniqueIdProperty,
    UrlProperty,
    VerificationProperty,
    LastEditedTimeProperty,
)


# PageObjectResponse の properties で使用されるプロパティ値の型
PropertyType = Union[
    ButtonProperty,
    CheckboxProperty,
    CreatedByProperty,
    CreatedTimeProperty,
    DateProperty,
    EmailProperty,
    FormulaProperty,
    FilesProperty,
    LastEditedByProperty,
    LastEditedTimeProperty,
    MultiSelectProperty,
    NumberProperty,
    PeopleProperty,
    PhoneNumberProperty,
    RichTextProperty,
    SelectProperty,
    StatusProperty,
    TitleProperty,
    UniqueIdProperty,
    UrlProperty,
    VerificationProperty,
    RelationProperty,
    RollupProperty,
]
