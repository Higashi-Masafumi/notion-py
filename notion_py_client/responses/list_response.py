"""
Notionリストレスポンス型の定義

TypeScript定義: ListUsersResponse, QueryDatabaseResponse, ListBlockChildrenResponse等
"""

from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, Field, StrictBool, StrictStr

from .page import NotionPage, PartialPage
from .database import NotionDatabase, PartialDatabase
from .datasource import DataSource, PartialDataSource
from ..models.user import PartialUser

T = TypeVar("T")


class ListResponse(BaseModel, Generic[T]):
    """汎用リストレスポンス.

    Notionの全てのリストAPIで共通のページネーション構造。

    Attributes:
        object: 常に "list"
        results: 結果の配列
        next_cursor: 次のページのカーソル（なければNone）
        has_more: さらにページがあるかどうか

    Examples:
        >>> response = await client.databases.query({"database_id": "abc"})
        >>> print(f"Has more: {response.has_more}")
        >>> for page in response.results:
        ...     print(page.id)
    """

    object: Literal["list"] = Field(..., description="オブジェクトタイプ")
    results: list[T] = Field(..., description="結果の配列")
    next_cursor: StrictStr | None = Field(None, description="次のページのカーソル")
    has_more: StrictBool = Field(..., description="さらにページがあるか")
    type: StrictStr | None = Field(
        None, description="結果の型ヒント（例: 'page_or_database'）"
    )


# 具体的なリストレスポンス型
class QueryDatabaseResponse(ListResponse[NotionPage]):
    """databases.query() のレスポンス型.

    Examples:
        >>> response = await client.databases.query({"database_id": "abc"})
        >>> pages: list[NotionPage] = response.results
        >>> if response.has_more:
        ...     next_response = await client.databases.query({
        ...         "database_id": "abc",
        ...         "start_cursor": response.next_cursor
        ...     })
    """

    type: Literal["page_or_database"] = Field("page_or_database", description="結果型")


class QueryDataSourceResponse(
    ListResponse[NotionPage | PartialPage | DataSource | PartialDataSource]
):
    """dataSources.query() のレスポンス型."""

    type: Literal["page_or_data_source"] = Field(
        "page_or_data_source", description="結果型"
    )


class ListUsersResponse(ListResponse[PartialUser]):
    """users.list() のレスポンス型."""

    type: Literal["user"] = Field("user", description="結果型")


class SearchResponse(
    ListResponse[NotionPage | PartialPage | NotionDatabase | PartialDatabase]
):
    """search() のレスポンス型."""

    type: Literal["page_or_database"] = Field("page_or_database", description="結果型")
