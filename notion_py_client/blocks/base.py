"""
Notionブロックの基底クラスと共通モデル
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, StrictBool, StrictStr

from ..models.parent import NotionParent
from ..models.user import PartialUser

# BlockType as Literal (TypeScript-style)
BlockType = Literal[
    "paragraph",
    "heading_1",
    "heading_2",
    "heading_3",
    "bulleted_list_item",
    "numbered_list_item",
    "quote",
    "to_do",
    "toggle",
    "template",
    "synced_block",
    "child_page",
    "child_database",
    "equation",
    "code",
    "callout",
    "divider",
    "breadcrumb",
    "table_of_contents",
    "column_list",
    "column",
    "link_to_page",
    "table",
    "table_row",
    "embed",
    "bookmark",
    "image",
    "video",
    "pdf",
    "file",
    "audio",
    "link_preview",
    "unsupported",
]

# ApiColor as Literal (TypeScript-style)
ApiColor = Literal[
    "default",
    "gray",
    "brown",
    "orange",
    "yellow",
    "green",
    "blue",
    "purple",
    "pink",
    "red",
    "default_background",
    "gray_background",
    "brown_background",
    "orange_background",
    "yellow_background",
    "green_background",
    "blue_background",
    "purple_background",
    "pink_background",
    "red_background",
]


class BaseBlockObject(BaseModel):
    """
    すべてのブロックタイプに共通のフィールド

    各ブロックタイプは、このクラスを継承し、
    `type`フィールドをLiteralで定義します。
    """

    object: Literal["block"] = Field("block", description="オブジェクトタイプ")
    id: StrictStr = Field(..., description="ブロックID")
    # type field is defined in each subclass with specific Literal
    created_time: StrictStr = Field(..., description="作成日時（ISO 8601形式）")
    created_by: PartialUser = Field(..., description="作成者")
    last_edited_time: StrictStr = Field(..., description="最終編集日時（ISO 8601形式）")
    last_edited_by: PartialUser = Field(..., description="最終編集者")
    parent: NotionParent = Field(..., description="親オブジェクト")
    has_children: StrictBool = Field(False, description="子ブロックの有無")
    archived: StrictBool = Field(False, description="アーカイブフラグ")
    in_trash: StrictBool = Field(False, description="ゴミ箱フラグ")


class PartialBlock(BaseModel):
    """部分的なブロック情報"""

    object: Literal["block"] = Field("block", description="オブジェクトタイプ")
    id: StrictStr = Field(..., description="ブロックID")
