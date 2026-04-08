"""Page creation and update request types.

Page作成・更新用のリクエストパラメータ型定義。
"""

from typing import Any, Literal

from pydantic import BaseModel, StrictBool, StrictStr

from ..models.parent import NotionParent
from .common import IdRequest, PageIconRequest, PageCoverRequest, TimeZoneRequest
from .property_requests import PropertyRequest


class PageTemplateRequest(BaseModel):
    """ページテンプレート適用設定."""

    type: Literal["none", "default", "template_id"]
    template_id: IdRequest | None = None
    timezone: TimeZoneRequest | None = None


class InsertContentMarkdownRequest(BaseModel):
    """既存ページのMarkdown末尾/指定位置挿入."""

    content: str
    after: StrictStr | None = None


class ReplaceContentRangeMarkdownRequest(BaseModel):
    """既存ページのMarkdown範囲置換."""

    content: str
    content_range: str
    allow_deleting_content: StrictBool | None = None


class MarkdownContentUpdateOperation(BaseModel):
    """search-and-replace 単位の更新."""

    old_str: str
    new_str: str
    replace_all_matches: StrictBool | None = None


class UpdateContentMarkdownRequest(BaseModel):
    """search-and-replace によるMarkdown更新."""

    content_updates: list[MarkdownContentUpdateOperation]
    allow_deleting_content: StrictBool | None = None


class ReplaceContentMarkdownRequest(BaseModel):
    """ページ全体のMarkdown置換."""

    new_str: str
    allow_deleting_content: StrictBool | None = None


class UpdatePageMarkdownParameters(BaseModel):
    """Markdownエンドポイント用パラメータ."""

    type: Literal[
        "insert_content",
        "replace_content_range",
        "update_content",
        "replace_content",
    ]
    insert_content: InsertContentMarkdownRequest | None = None
    replace_content_range: ReplaceContentRangeMarkdownRequest | None = None
    update_content: UpdateContentMarkdownRequest | None = None
    replace_content: ReplaceContentMarkdownRequest | None = None


class CreatePageParameters(BaseModel):
    """Page作成用パラメータ.

    Examples:
        >>> params = CreatePageParameters(
        ...     parent={"database_id": "xxx"},
        ...     properties={
        ...         "Name": {"title": [{"text": {"content": "My Page"}}]},
        ...         "Status": {"select": {"name": "In Progress"}},
        ...     }
        ... )
    """

    parent: NotionParent
    properties: dict[str, PropertyRequest]
    icon: PageIconRequest | None = None
    cover: PageCoverRequest | None = None
    content: list[Any] | None = None  # BlockObjectRequest
    children: list[Any] | None = None  # BlockObjectRequest
    markdown: str | None = None
    template: PageTemplateRequest | None = None


class UpdatePageParameters(BaseModel):
    """Page更新用パラメータ.

    Examples:
        >>> params = UpdatePageParameters(
        ...     page_id="page-id-here",
        ...     properties={
        ...         "Status": {"select": {"name": "Done"}},
        ...         "Checkbox": {"checkbox": True},
        ...     }
        ... )
    """

    page_id: IdRequest
    properties: dict[str, PropertyRequest] | None = None
    icon: PageIconRequest | None = None
    cover: PageCoverRequest | None = None
    is_locked: StrictBool | None = None
    in_trash: StrictBool | None = None
    template: PageTemplateRequest | None = None
    erase_content: StrictBool | None = None
