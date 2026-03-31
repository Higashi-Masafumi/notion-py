"""Page creation and update request types.

Page作成・更新用のリクエストパラメータ型定義。
"""

from typing import Any

from pydantic import BaseModel, StrictBool, model_validator

from ..models.parent import NotionParent
from .common import IdRequest, PageIconRequest, PageCoverRequest
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
    content: list[Any] | None = None  # BlockObjectRequest
    children: list[Any] | None = None  # BlockObjectRequest


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
    archived: StrictBool | None = None
    in_trash: StrictBool | None = None

    @model_validator(mode="after")
    def normalize_trash_fields(self) -> "UpdatePageParameters":
        if self.in_trash is None and self.archived is not None:
            self.in_trash = self.archived
        if self.archived is None and self.in_trash is not None:
            self.archived = self.in_trash
        return self

    def model_dump(self, *args, **kwargs):
        payload = super().model_dump(*args, **kwargs)
        if payload.get("in_trash") is not None:
            payload.pop("archived", None)
        return payload
