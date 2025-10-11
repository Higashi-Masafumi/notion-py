"""Page creation and update request types.

Page作成・更新用のリクエストパラメータ型定義。
"""

from typing import Any

from pydantic import BaseModel, StrictBool

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
