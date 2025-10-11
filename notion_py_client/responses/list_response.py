"""
Notionリストレスポンス型の定義

TypeScript定義: ListUsersResponse, QueryDatabaseResponse, ListBlockChildrenResponse等
"""

from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, Field, StrictBool, StrictStr

from .page import NotionPage, PartialPage
from .database import NotionDatabase, PartialDatabase
from .datasource import DataSource, PartialDataSource
from .file_upload import FileUploadObject
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

    備考: リスト型の共通フィールド `type` は親クラスで定義済み。
    サブクラスではオーバーライドしない（LSP/型チェッカー警告を避ける）。
    """


class QueryDataSourceResponse(
    ListResponse[NotionPage | PartialPage | DataSource | PartialDataSource]
):
    """dataSources.query() のレスポンス型.

    備考: `type` は親クラス側の型（StrictStr | None）を使用。
    """


class ListUsersResponse(ListResponse[PartialUser]):
    """users.list() のレスポンス型.

    備考: `type` は親クラスに準拠。
    """


class SearchResponse(
    ListResponse[NotionPage | PartialPage | NotionDatabase | PartialDatabase]
):
    """search() のレスポンス型.

    備考: `type` は親クラスに準拠。
    """


class ListFileUploadsResponse(ListResponse[FileUploadObject]):
    """file_uploads.list() のレスポンス型.

    備考: `type` は親クラスに準拠（省略される場合あり）。
    """
