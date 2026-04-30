"""Page creation and update request types.

Page作成・更新用のリクエストパラメータ型定義。
"""

from typing import Any, Literal

from pydantic import BaseModel, StrictBool, model_validator

from ..models.parent import NotionParent
from .common import (
    IdRequest,
    PageCoverRequest,
    PageIconRequest,
    PagePositionRequest,
    PageTemplateRequest,
)
from .property_requests import PropertyRequest


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
    template: PageTemplateRequest | None = None
    position: PagePositionRequest | None = None
    markdown: str | None = None
    content: list[Any] | None = None  # BlockObjectRequest
    children: list[Any] | None = None  # BlockObjectRequest

    @model_validator(mode="after")
    def validate_body_modes(self) -> "CreatePageParameters":
        if self.markdown is not None and (
            self.content is not None or self.children is not None
        ):
            raise ValueError("markdown cannot be used with content or children")
        if self.template is not None and (
            self.content is not None or self.children is not None
        ):
            raise ValueError("template cannot be used with content or children")
        return self


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
    template: PageTemplateRequest | None = None
    erase_content: StrictBool | None = None
    is_locked: StrictBool | None = None
    in_trash: StrictBool | None = None


class MarkdownContentUpdateRequest(BaseModel):
    """Search-and-replace operation for markdown page updates."""

    old_str: str
    new_str: str
    replace_all_matches: StrictBool | None = None


class UpdateContentMarkdownRequest(BaseModel):
    """Update markdown content using targeted replacements."""

    content_updates: list[MarkdownContentUpdateRequest]
    allow_deleting_content: StrictBool | None = None


class UpdateContentMarkdownCommand(BaseModel):
    """PATCH /pages/{page_id}/markdown with update_content."""

    type: Literal["update_content"] = "update_content"
    update_content: UpdateContentMarkdownRequest


class ReplaceContentMarkdownRequest(BaseModel):
    """Replace the entire page markdown content."""

    new_str: str
    allow_deleting_content: StrictBool | None = None


class ReplaceContentMarkdownCommand(BaseModel):
    """PATCH /pages/{page_id}/markdown with replace_content."""

    type: Literal["replace_content"] = "replace_content"
    replace_content: ReplaceContentMarkdownRequest


class InsertContentMarkdownRequest(BaseModel):
    """Legacy insert_content markdown command."""

    content: str
    after: str | None = None


class InsertContentMarkdownCommand(BaseModel):
    """PATCH /pages/{page_id}/markdown with insert_content."""

    type: Literal["insert_content"] = "insert_content"
    insert_content: InsertContentMarkdownRequest


class ReplaceContentRangeMarkdownRequest(BaseModel):
    """Legacy replace_content_range markdown command."""

    content: str
    content_range: str
    allow_deleting_content: StrictBool | None = None


class ReplaceContentRangeMarkdownCommand(BaseModel):
    """PATCH /pages/{page_id}/markdown with replace_content_range."""

    type: Literal["replace_content_range"] = "replace_content_range"
    replace_content_range: ReplaceContentRangeMarkdownRequest


PageMarkdownCommand = (
    UpdateContentMarkdownCommand
    | ReplaceContentMarkdownCommand
    | InsertContentMarkdownCommand
    | ReplaceContentRangeMarkdownCommand
)
