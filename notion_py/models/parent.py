"""
Notion親オブジェクトモデル

Database、Page、DataSource、Blockなどで使用される親オブジェクトの定義
"""

from __future__ import annotations

from typing import Literal, TypedDict, NotRequired


class DatabaseParent(TypedDict):
    """データベースを親とするオブジェクト.

    Examples:
        >>> parent: DatabaseParent = {
        ...     "type": "database_id",
        ...     "database_id": "abc123"
        ... }
    """

    type: Literal["database_id"]
    database_id: str


class PageParent(TypedDict):
    """ページを親とするオブジェクト.

    Examples:
        >>> parent: PageParent = {
        ...     "type": "page_id",
        ...     "page_id": "abc123"
        ... }
    """

    type: Literal["page_id"]
    page_id: str


class WorkspaceParent(TypedDict):
    """ワークスペースを親とするオブジェクト.

    Examples:
        >>> parent: WorkspaceParent = {
        ...     "type": "workspace",
        ...     "workspace": True
        ... }
    """

    type: Literal["workspace"]
    workspace: Literal[True]


class BlockParent(TypedDict):
    """ブロックを親とするオブジェクト.

    Examples:
        >>> parent: BlockParent = {
        ...     "type": "block_id",
        ...     "block_id": "abc123"
        ... }
    """

    type: Literal["block_id"]
    block_id: str


class DataSourceParent(TypedDict):
    """データソースを親とするオブジェクト.

    Examples:
        >>> parent: DataSourceParent = {
        ...     "type": "data_source_id",
        ...     "data_source_id": "abc123"
        ... }
    """

    type: Literal["data_source_id"]
    data_source_id: str


# すべての親タイプのUnion型
NotionParent = (
    DatabaseParent | PageParent | WorkspaceParent | BlockParent | DataSourceParent
)
