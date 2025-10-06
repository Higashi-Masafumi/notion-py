"""
Notionブロックの基底クラスと共通モデル
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, StrictBool, StrictStr

from ..models.user import PartialUser
from ..models.parent import NotionParent


class BlockType(str, Enum):
    """ブロックタイプ"""

    PARAGRAPH = "paragraph"
    HEADING_1 = "heading_1"
    HEADING_2 = "heading_2"
    HEADING_3 = "heading_3"
    BULLETED_LIST_ITEM = "bulleted_list_item"
    NUMBERED_LIST_ITEM = "numbered_list_item"
    QUOTE = "quote"
    TO_DO = "to_do"
    TOGGLE = "toggle"
    TEMPLATE = "template"
    SYNCED_BLOCK = "synced_block"
    CHILD_PAGE = "child_page"
    CHILD_DATABASE = "child_database"
    EQUATION = "equation"
    CODE = "code"
    CALLOUT = "callout"
    DIVIDER = "divider"
    BREADCRUMB = "breadcrumb"
    TABLE_OF_CONTENTS = "table_of_contents"
    COLUMN_LIST = "column_list"
    COLUMN = "column"
    LINK_TO_PAGE = "link_to_page"
    TABLE = "table"
    TABLE_ROW = "table_row"
    EMBED = "embed"
    BOOKMARK = "bookmark"
    IMAGE = "image"
    VIDEO = "video"
    PDF = "pdf"
    FILE = "file"
    AUDIO = "audio"
    LINK_PREVIEW = "link_preview"
    UNSUPPORTED = "unsupported"


class ApiColor(str, Enum):
    """
    Notionのカラー設定

    テキストカラーと背景カラーの両方を含む
    """

    DEFAULT = "default"
    GRAY = "gray"
    BROWN = "brown"
    ORANGE = "orange"
    YELLOW = "yellow"
    GREEN = "green"
    BLUE = "blue"
    PURPLE = "purple"
    PINK = "pink"
    RED = "red"
    DEFAULT_BACKGROUND = "default_background"
    GRAY_BACKGROUND = "gray_background"
    BROWN_BACKGROUND = "brown_background"
    ORANGE_BACKGROUND = "orange_background"
    YELLOW_BACKGROUND = "yellow_background"
    GREEN_BACKGROUND = "green_background"
    BLUE_BACKGROUND = "blue_background"
    PURPLE_BACKGROUND = "purple_background"
    PINK_BACKGROUND = "pink_background"
    RED_BACKGROUND = "red_background"


class BaseBlockObject(BaseModel):
    """
    すべてのブロックタイプに共通のフィールド

    各ブロックタイプは、このクラスを継承し、
    `type`フィールドをLiteralでオーバーライドします。
    """

    object: Literal["block"] = Field("block", description="オブジェクトタイプ")
    id: StrictStr = Field(..., description="ブロックID")
    type: BlockType = Field(..., description="ブロックタイプ")
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
