"""Notion API パラメータの型定義.

公式TypeScript SDKの型定義に準拠したパラメータ型を提供します。
TypedDictを使用して、dict リテラルでIDE補完をサポートします。

References:
    - https://github.com/makenotion/notion-sdk-js/blob/main/src/api-endpoints.ts
"""

from typing import TypedDict, NotRequired, Literal, Any

from .filters import FilterCondition


# ========== Database API Types ==========
class DatabaseQuerySort(TypedDict, total=False):
    """データベースクエリのソート条件.

    References:
        - https://github.com/makenotion/notion-sdk-js/blob/main/src/api-endpoints.ts#L1234
    """

    property: NotRequired[str]
    direction: NotRequired[Literal["ascending", "descending"]]
    timestamp: NotRequired[Literal["created_time", "last_edited_time"]]


class _QueryDatabaseRequired(TypedDict):
    """QueryDatabaseParametersの必須フィールド."""

    database_id: str


class QueryDatabaseParameters(_QueryDatabaseRequired, total=False):
    """データベースクエリのパラメータ.

    References:
        - https://github.com/makenotion/notion-sdk-js/blob/main/src/api-endpoints.ts#L123

    Example:
        >>> params: QueryDatabaseParameters = {
        ...     "database_id": "abc123",
        ...     "filter": PropertyFilterStatus(property="Status", status=StatusFilterEquals(equals="Active")),
        ...     "page_size": 50,
        ... }
        >>> results = await client.databases.query(params)
    """

    filter: FilterCondition | dict[str, Any]
    sorts: list[DatabaseQuerySort]
    start_cursor: str
    page_size: int
    filter_properties: list[str]
    archived: bool


class RetrieveDatabaseParameters(TypedDict):
    """データベース取得のパラメータ.

    References:
        - https://github.com/makenotion/notion-sdk-js/blob/main/src/api-endpoints.ts#L456
    """

    database_id: str


class _CreateDatabaseRequired(TypedDict):
    """CreateDatabaseParametersの必須フィールド."""

    parent: dict[str, str]
    properties: dict[str, Any]


class CreateDatabaseParameters(_CreateDatabaseRequired, total=False):
    """データベース作成のパラメータ.

    References:
        - https://github.com/makenotion/notion-sdk-js/blob/main/src/api-endpoints.ts#L789
    """

    title: list[dict[str, Any]]
    icon: dict[str, Any]
    cover: dict[str, Any]
    is_inline: bool


class _UpdateDatabaseRequired(TypedDict):
    """UpdateDatabaseParametersの必須フィールド."""

    database_id: str


class UpdateDatabaseParameters(_UpdateDatabaseRequired, total=False):
    """データベース更新のパラメータ.

    References:
        - https://github.com/makenotion/notion-sdk-js/blob/main/src/api-endpoints.ts#L1011
    """

    properties: dict[str, Any]
    title: list[dict[str, Any]]
    description: list[dict[str, Any]]
    icon: dict[str, Any]
    cover: dict[str, Any]


# ========== Search API Types ==========
class SearchParameters(TypedDict, total=False):
    """検索のパラメータ.

    References:
        - https://github.com/makenotion/notion-sdk-js/blob/main/src/api-endpoints.ts#L2345
    """

    query: NotRequired[str]
    filter: NotRequired[dict[str, str]]
    sort: NotRequired[dict[str, str]]
    start_cursor: NotRequired[str]
    page_size: NotRequired[int]


# ========== Page API Types ==========
class _RetrievePageRequired(TypedDict):
    """RetrievePageParametersの必須フィールド."""

    page_id: str


class RetrievePageParameters(_RetrievePageRequired, total=False):
    """ページ取得のパラメータ."""

    filter_properties: list[str]


class _CreatePageRequired(TypedDict):
    """CreatePageParametersの必須フィールド."""

    parent: dict[str, str]
    properties: dict[str, Any]


class CreatePageParameters(_CreatePageRequired, total=False):
    """ページ作成のパラメータ."""

    children: list[dict[str, Any]]
    icon: dict[str, Any]
    cover: dict[str, Any]


class _UpdatePageRequired(TypedDict):
    """UpdatePageParametersの必須フィールド."""

    page_id: str


class UpdatePageParameters(_UpdatePageRequired, total=False):
    """ページ更新のパラメータ."""

    properties: dict[str, Any]
    archived: bool
    icon: dict[str, Any]
    cover: dict[str, Any]


# ========== Block API Types ==========
class RetrieveBlockParameters(TypedDict):
    """ブロック取得のパラメータ."""

    block_id: str


class UpdateBlockParameters(TypedDict, total=False):
    """ブロック更新のパラメータ."""

    block_id: str
    archived: NotRequired[bool]


class DeleteBlockParameters(TypedDict):
    """ブロック削除のパラメータ."""

    block_id: str


class ListBlockChildrenParameters(TypedDict, total=False):
    """ブロックの子要素リスト取得のパラメータ."""

    block_id: str
    start_cursor: NotRequired[str]
    page_size: NotRequired[int]


class AppendBlockChildrenParameters(TypedDict, total=False):
    """ブロックの子要素追加のパラメータ."""

    block_id: str
    children: list[dict[str, Any]]
    after: NotRequired[str]


# ========== User API Types ==========
class RetrieveUserParameters(TypedDict):
    """ユーザー取得のパラメータ."""

    user_id: str


class ListUsersParameters(TypedDict, total=False):
    """ユーザーリスト取得のパラメータ."""

    start_cursor: NotRequired[str]
    page_size: NotRequired[int]


# ========== Comment API Types ==========
class CreateCommentParameters(TypedDict, total=False):
    """コメント作成のパラメータ."""

    parent: dict[str, str]
    rich_text: list[dict[str, Any]]
    discussion_id: NotRequired[str]


class ListCommentsParameters(TypedDict, total=False):
    """コメントリスト取得のパラメータ."""

    block_id: NotRequired[str]
    start_cursor: NotRequired[str]
    page_size: NotRequired[int]
