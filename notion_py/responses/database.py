"""
NotionデータベースオブジェクトのPydanticモデル定義

TypeScript定義: DatabaseObjectResponse
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, StrictBool, StrictStr
from typing_extensions import TypedDict

from ..models.parent import NotionParent
from ..models.icon import NotionIcon
from ..models.cover import NotionCover
from ..schema.property_configs import DatabasePropertyConfigResponse


class DataSourceReference(TypedDict):
    """データソース参照情報 (2025-09-03で追加)"""

    id: str
    name: str


class NotionDatabase(BaseModel):
    """
    Notionデータベースオブジェクト

    TypeScript: DatabaseObjectResponse

    **重要**: NotionDatabase はデータベース全体のコンテナです。
    データベース内のデータ行を取得するには databases.query() を使用してください。

    用途:
    - データベース全体のメタ情報（タイトル、説明、アイコンなど）
    - データベースのスキーマ定義（properties）
    - データベースの親情報

    取得方法:
    - databases.retrieve(database_id) でデータベース情報を取得
    - databases.create() で新規データベースを作成
    - databases.update() でデータベースを更新

    データ取得:
    - databases.query(database_id) でデータベース内のページ（NotionPage）を取得

    Examples:
        ```python
        # データベース情報を取得
        db = await client.databases.retrieve({"database_id": "abc123"})

        # データベースのタイトルを取得
        if db.title:
            title_text = "".join([t.plain_text for t in db.title])
            print(f"Database: {title_text}")

        # スキーマ定義を確認
        for name, config in db.properties.items():
            print(f"Property: {name}, Type: {config.type}")

        # データベース内のページを取得
        pages = await client.databases.query({"database_id": db.id})
        ```
    """

    object: Literal["database"] = Field(..., description="オブジェクトタイプ")
    id: StrictStr = Field(..., description="データベースID")
    title: list[Any] = Field(..., description="データベースタイトル（RichText配列）")
    description: list[Any] = Field(
        default_factory=list, description="データベース説明（RichText配列）"
    )
    parent: NotionParent = Field(..., description="親オブジェクト")
    is_inline: StrictBool = Field(False, description="インラインデータベースフラグ")
    in_trash: StrictBool = Field(False, description="ゴミ箱フラグ")
    is_locked: StrictBool = Field(False, description="ロックフラグ")
    created_time: StrictStr = Field(..., description="作成日時（ISO 8601形式）")
    last_edited_time: StrictStr = Field(..., description="最終編集日時（ISO 8601形式）")
    data_sources: list[DataSourceReference] = Field(
        default_factory=list, description="データソース一覧（2025-09-03以降）"
    )
    icon: NotionIcon | None = Field(None, description="アイコン")
    cover: NotionCover | None = Field(None, description="カバー画像")
    url: StrictStr = Field(..., description="データベースURL")
    public_url: StrictStr | None = Field(None, description="パブリックURL")
    properties: dict[str, DatabasePropertyConfigResponse] | None = Field(
        None,
        description="プロパティ設定の辞書 (2025-09-03以降はdataSources.retrieve()で取得)",
    )
    # archived フィールドは TypeScript 定義にない（削除）


class PartialDatabase(BaseModel):
    """部分的なデータベース情報"""

    object: Literal["database"] = Field(..., description="オブジェクトタイプ")
    id: StrictStr = Field(..., description="データベースID")
