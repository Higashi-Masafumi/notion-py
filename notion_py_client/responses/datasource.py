"""
NotionデータソースオブジェクトのPydanticモデル定義

TypeScript定義: DataSourceObjectResponse

データソースは、データベース内のビュー/テーブルの構造を定義します。
PageObjectResponse とは異なり、スキーマ定義を持ちます。
"""

from typing import Any, Literal

from pydantic import BaseModel, Field, StrictBool, StrictStr

from ..models.user import PartialUser
from ..models.icon import NotionIcon
from ..models.cover import NotionCover
from ..models.parent import NotionParent
from ..schema.property_configs import DatabasePropertyConfigResponse


class DataSource(BaseModel):
    """
    Notionデータソースオブジェクト

    TypeScript: DataSourceObjectResponse

    **重要**: DataSourceはデータベースのスキーマ定義（メタ情報）です。
    データベースの実際のデータ行（レコード）は NotionPage です。

    用途:
    - データベース内のビューやテーブルの構造を定義
    - properties には DatabasePropertyConfigResponse が入る（スキーマ定義）
    - データ取得には pages API や databases.query() を使用（NotionPage を返す）

    取得方法:
    - dataSources.retrieve(data_source_id) でスキーマ情報を取得
    - databases.query(database_id) はデータ行（NotionPage）を返す

    Examples:
        ```python
        # データソース（スキーマ）を取得
        datasource = await client.dataSources.retrieve({
            "data_source_id": "abc123"
        })

        # properties にはスキーマ定義が入っている
        for name, config in datasource.properties.items():
            print(f"Property: {name}, Type: {config.type}")
        ```
    """

    object: Literal["data_source"] = Field(..., description="オブジェクトタイプ")
    id: StrictStr = Field(..., description="データソースID")
    title: list[Any] = Field(..., description="データソースタイトル（RichText配列）")
    description: list[Any] = Field(
        default_factory=list, description="データソース説明（RichText配列）"
    )
    parent: NotionParent = Field(..., description="親オブジェクト")
    database_parent: NotionParent = Field(
        ..., description="データベースの親オブジェクト"
    )
    is_inline: StrictBool = Field(False, description="インラインフラグ")
    archived: StrictBool = Field(False, description="アーカイブフラグ")
    in_trash: StrictBool = Field(False, description="ゴミ箱フラグ")
    created_time: StrictStr = Field(..., description="作成日時（ISO 8601形式）")
    last_edited_time: StrictStr = Field(..., description="最終編集日時（ISO 8601形式）")
    created_by: PartialUser = Field(..., description="作成者")
    last_edited_by: PartialUser = Field(..., description="最終編集者")
    properties: dict[str, DatabasePropertyConfigResponse] = Field(
        ..., description="プロパティスキーマ定義"
    )
    icon: NotionIcon | None = Field(None, description="アイコン")
    cover: NotionCover | None = Field(None, description="カバー画像")
    url: StrictStr = Field(..., description="データソースURL")
    public_url: StrictStr | None = Field(None, description="パブリックURL")


class PartialDataSource(BaseModel):
    """部分的なデータソース情報"""

    object: Literal["data_source"] = Field(..., description="オブジェクトタイプ")
    id: StrictStr = Field(..., description="データソースID")
    properties: dict[str, DatabasePropertyConfigResponse] = Field(
        ..., description="プロパティスキーマ定義"
    )
