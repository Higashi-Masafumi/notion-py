"""Property request types for creating/updating Notion pages.

Page作成・更新時に使用するプロパティ値のリクエスト型定義。
TypeScript SDKの `UpdatePageBodyParameters.properties` に対応。

Note:
    以下のプロパティ型は読み取り専用のため、Request型は存在しません:
    - Formula (計算式による自動生成)
    - Rollup (他プロパティの集計)
    - CreatedBy, CreatedTime (作成情報)
    - LastEditedBy, LastEditedTime (更新情報)
    - UniqueId (自動生成ID)
    - Button (アクション用)
    - Verification (検証用)
"""

from typing import Any, Literal, Union

from pydantic import BaseModel

from .common import (
    DateRequest,
    GroupObjectRequest,
    IdRequest,
    PartialUserObjectRequest,
    RelationItemRequest,
    SelectPropertyItemRequest,
    StringRequest,
    TextRequest,
)


class TitlePropertyRequest(BaseModel):
    """Titleプロパティのリクエスト."""

    title: list[Any]  # RichTextItemRequest
    type: Literal["title"] | None = None


class RichTextPropertyRequest(BaseModel):
    """RichTextプロパティのリクエスト."""

    rich_text: list[Any]  # RichTextItemRequest
    type: Literal["rich_text"] | None = None


class NumberPropertyRequest(BaseModel):
    """Numberプロパティのリクエスト."""

    number: float | None
    type: Literal["number"] | None = None


class UrlPropertyRequest(BaseModel):
    """URLプロパティのリクエスト."""

    url: TextRequest | None
    type: Literal["url"] | None = None


class SelectPropertyRequest(BaseModel):
    """Selectプロパティのリクエスト.

    選択肢をIDまたは名前で指定可能。
    Noneの場合は選択解除。
    """

    select: SelectPropertyItemRequest | None
    type: Literal["select"] | None = None


class MultiSelectPropertyRequest(BaseModel):
    """MultiSelectプロパティのリクエスト.

    複数の選択肢をIDまたは名前で指定可能。
    """

    multi_select: list[SelectPropertyItemRequest]
    type: Literal["multi_select"] | None = None


class StatusPropertyRequest(BaseModel):
    """Statusプロパティのリクエスト.

    ステータスをIDまたは名前で指定可能。
    Noneの場合はステータス解除。
    """

    status: SelectPropertyItemRequest | None
    type: Literal["status"] | None = None


class PeoplePropertyRequest(BaseModel):
    """Peopleプロパティのリクエスト.

    ユーザーまたはグループを指定可能。
    """

    people: list[PartialUserObjectRequest | GroupObjectRequest]
    type: Literal["people"] | None = None


class EmailPropertyRequest(BaseModel):
    """Emailプロパティのリクエスト."""

    email: StringRequest | None
    type: Literal["email"] | None = None


class PhoneNumberPropertyRequest(BaseModel):
    """PhoneNumberプロパティのリクエスト."""

    phone_number: StringRequest | None
    type: Literal["phone_number"] | None = None


class DatePropertyRequest(BaseModel):
    """Dateプロパティのリクエスト."""

    date: DateRequest | None
    type: Literal["date"] | None = None


class CheckboxPropertyRequest(BaseModel):
    """Checkboxプロパティのリクエスト."""

    checkbox: bool
    type: Literal["checkbox"] | None = None


class RelationPropertyRequest(BaseModel):
    """Relationプロパティのリクエスト.

    関連するページのIDのリストを指定。
    """

    relation: list[RelationItemRequest]
    type: Literal["relation"] | None = None


class FilesPropertyRequest(BaseModel):
    """Filesプロパティのリクエスト."""

    files: list[
        Any
    ]  # InternalOrExternalFileWithNameRequest | FileUploadWithOptionalNameRequest
    type: Literal["files"] | None = None


# すべてのプロパティリクエストのUnion型
PropertyRequest = Union[
    TitlePropertyRequest,
    RichTextPropertyRequest,
    NumberPropertyRequest,
    UrlPropertyRequest,
    SelectPropertyRequest,
    MultiSelectPropertyRequest,
    StatusPropertyRequest,
    PeoplePropertyRequest,
    EmailPropertyRequest,
    PhoneNumberPropertyRequest,
    DatePropertyRequest,
    CheckboxPropertyRequest,
    RelationPropertyRequest,
    FilesPropertyRequest,
]
