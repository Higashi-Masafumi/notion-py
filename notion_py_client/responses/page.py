"""
NotionページオブジェクトのPydanticモデル定義

TypeScript定義: PageObjectResponse

ページオブジェクトは、pages.retrieve APIなどで返される型です。
基本的にはDataSourceObjectResponseと同じ構造ですが、
より豊富な情報を含む可能性があります。
"""

from typing import Literal

from pydantic import BaseModel, Field, StrictBool, StrictStr

from ..models.user import PartialUser
from ..models.icon import NotionIcon
from ..models.cover import NotionCover
from ..models.parent import NotionParent
from .property_types import PropertyType


class NotionPage(BaseModel):
    """
    Notionページオブジェクト

    TypeScript: PageObjectResponse

    **重要**: NotionPage はデータベース内の実際のデータ行（レコード）、
    または通常のNotionページです。

    用途:
    - データベース内の1行のデータ
    - 通常のNotionページ
    - properties には実際のプロパティ値が入る

    取得方法:
    - pages.retrieve(page_id) で個別のページを取得
    - databases.query(database_id) でデータベース内のページ一覧を取得
    - pages.create() で新規ページを作成
    - pages.update() でページを更新

    Examples:
        ```python
        # ページを取得
        page = await client.pages.retrieve({"page_id": "abc123"})

        # プロパティにアクセス（実際の値が入っている）
        title_prop = page.properties.get("名前")
        if title_prop and hasattr(title_prop, "get_value"):
            title = title_prop.get_value()
            print(f"Title: {title}")

        # メタデータにアクセス
        print(f"Created: {page.created_time}")
        print(f"URL: {page.url}")
        ```
    """

    object: Literal["page"] = Field(..., description="オブジェクトタイプ")
    id: StrictStr = Field(..., description="ページID")
    created_time: StrictStr = Field(..., description="作成日時（ISO 8601形式）")
    last_edited_time: StrictStr = Field(..., description="最終編集日時（ISO 8601形式）")
    created_by: PartialUser = Field(..., description="作成者")
    last_edited_by: PartialUser = Field(..., description="最終編集者")
    parent: NotionParent = Field(..., description="親オブジェクト")
    archived: StrictBool = Field(False, description="アーカイブフラグ")
    in_trash: StrictBool = Field(False, description="ゴミ箱フラグ")
    is_locked: StrictBool = Field(False, description="ロックフラグ")
    properties: dict[str, PropertyType] = Field(..., description="プロパティ一覧")
    icon: NotionIcon | None = Field(None, description="アイコン")
    cover: NotionCover | None = Field(None, description="カバー画像")
    url: StrictStr = Field(..., description="ページURL")
    public_url: StrictStr | None = Field(None, description="パブリックURL")

    # ページ固有のプロパティ（オプション）
    request_id: StrictStr | None = Field(None, description="リクエストID")


class PartialPage(BaseModel):
    """部分的なページ情報"""

    object: Literal["page"] = Field(..., description="オブジェクトタイプ")
    id: StrictStr = Field(..., description="ページID")
