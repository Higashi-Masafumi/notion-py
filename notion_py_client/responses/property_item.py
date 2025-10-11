"""
PropertyItemObjectResponse と PropertyItemListResponse の型定義
"""

from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, Field, StrictBool, StrictStr

from ..models.date_info import DateInfo
from ..models.file import FileWithName
from ..models.rich_text_item import RichTextItem
from ..models.user import PartialUser, User
from ..properties.rollup_property import Rollup
from ..models.formula import FormulaResult
from ..models.unique_id import UniqueId
from ..models.verification import Verification
from ..models.select_option import SelectOption


# 単一プロパティアイテム
class _BasePropertyItem(BaseModel):
    object: Literal["property_item"] = Field("property_item", description="型名")
    id: StrictStr


class NumberPropertyItem(_BasePropertyItem):
    type: Literal["number"]
    number: float | None


class UrlPropertyItem(_BasePropertyItem):
    type: Literal["url"]
    url: StrictStr | None


class SelectPropertyItem(_BasePropertyItem):
    type: Literal["select"]
    select: SelectOption | None


class MultiSelectPropertyItem(_BasePropertyItem):
    type: Literal["multi_select"]
    multi_select: list[SelectOption]


class StatusPropertyItem(_BasePropertyItem):
    type: Literal["status"]
    status: SelectOption | None


class DatePropertyItem(_BasePropertyItem):
    type: Literal["date"]
    date: DateInfo | None


class EmailPropertyItem(_BasePropertyItem):
    type: Literal["email"]
    email: StrictStr | None


class PhoneNumberPropertyItem(_BasePropertyItem):
    type: Literal["phone_number"]
    phone_number: StrictStr | None


class CheckboxPropertyItem(_BasePropertyItem):
    type: Literal["checkbox"]
    checkbox: StrictBool


class FilesPropertyItem(_BasePropertyItem):
    type: Literal["files"]
    files: list[FileWithName]


class CreatedByPropertyItem(_BasePropertyItem):
    type: Literal["created_by"]
    created_by: PartialUser | User


class CreatedTimePropertyItem(_BasePropertyItem):
    type: Literal["created_time"]
    created_time: StrictStr


class LastEditedByPropertyItem(_BasePropertyItem):
    type: Literal["last_edited_by"]
    last_edited_by: PartialUser | User


class LastEditedTimePropertyItem(_BasePropertyItem):
    type: Literal["last_edited_time"]
    last_edited_time: StrictStr


class FormulaPropertyItem(_BasePropertyItem):
    type: Literal["formula"]
    formula: FormulaResult


class ButtonPropertyItem(_BasePropertyItem):
    type: Literal["button"]
    button: dict


class UniqueIdPropertyItem(_BasePropertyItem):
    type: Literal["unique_id"]
    unique_id: UniqueId


class VerificationPropertyItem(_BasePropertyItem):
    type: Literal["verification"]
    verification: Verification | None


class TitlePropertyItem(_BasePropertyItem):
    type: Literal["title"]
    title: RichTextItem


class RichTextPropertyItem(_BasePropertyItem):
    type: Literal["rich_text"]
    rich_text: RichTextItem


class PeoplePropertyItem(_BasePropertyItem):
    type: Literal["people"]
    people: PartialUser | User


class RelationPropertyItem(_BasePropertyItem):
    type: Literal["relation"]
    relation: dict


class RollupPropertyItem(_BasePropertyItem):
    type: Literal["rollup"]
    rollup: Rollup | dict


PropertyItemObject = Union[
    NumberPropertyItem,
    UrlPropertyItem,
    SelectPropertyItem,
    MultiSelectPropertyItem,
    StatusPropertyItem,
    DatePropertyItem,
    EmailPropertyItem,
    PhoneNumberPropertyItem,
    CheckboxPropertyItem,
    FilesPropertyItem,
    CreatedByPropertyItem,
    CreatedTimePropertyItem,
    LastEditedByPropertyItem,
    LastEditedTimePropertyItem,
    FormulaPropertyItem,
    ButtonPropertyItem,
    UniqueIdPropertyItem,
    VerificationPropertyItem,
    TitlePropertyItem,
    RichTextPropertyItem,
    PeoplePropertyItem,
    RelationPropertyItem,
    RollupPropertyItem,
]


class _PropertyItemMeta(BaseModel):
    """Property items pagination meta used by pages.properties.retrieve"""

    type: Literal["property_item"]
    # title/rich_text/people/relation/rollup のときnext_url等を含む
    # 型バリエーションは仕様通りに構築するには複雑なのでここでは next_url と id のみ保持
    next_url: StrictStr | None
    id: StrictStr


class PropertyItemListResponse(BaseModel):
    object: Literal["list"]
    next_cursor: StrictStr | None
    has_more: StrictBool
    type: Literal["property_item"]
    property_item: _PropertyItemMeta
    results: list[PropertyItemObject]
