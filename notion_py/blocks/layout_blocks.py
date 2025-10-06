"""
レイアウト系ブロックの定義

Divider, Breadcrumb, TableOfContents, ColumnList, Column, LinkToPage, Table, TableRow
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr

from .base import ApiColor, BaseBlockObject, BlockType
from ..models.rich_text_item import RichTextItem


# ============================================
# Content Models
# ============================================


class EmptyObject(BaseModel):
    """空のオブジェクト"""

    pass


class TableOfContentsContent(BaseModel):
    """目次コンテンツ"""

    color: ApiColor = Field(..., description="カラー設定")


class ColumnContent(BaseModel):
    """カラムコンテンツ"""

    width_ratio: float | None = Field(
        None,
        description="カラムリスト内の全カラムに対するこのカラムの幅の比率（0〜1）。指定しない場合は等幅",
    )


class LinkToPageContent(BaseModel):
    """ページへのリンクコンテンツ"""

    type: Literal["page_id", "database_id", "comment_id"] = Field(
        ..., description="リンクタイプ"
    )
    page_id: StrictStr | None = Field(None, description="ページID")
    database_id: StrictStr | None = Field(None, description="データベースID")
    comment_id: StrictStr | None = Field(None, description="コメントID")


class TableContent(BaseModel):
    """テーブルコンテンツ"""

    has_column_header: StrictBool = Field(..., description="列ヘッダーの有無")
    has_row_header: StrictBool = Field(..., description="行ヘッダーの有無")
    table_width: StrictInt = Field(..., description="テーブルの幅")


class TableRowContent(BaseModel):
    """テーブル行コンテンツ"""

    cells: list[list[RichTextItem]] = Field(..., description="セル配列（2次元配列）")


# ============================================
# Layout Blocks
# ============================================


class DividerBlock(BaseBlockObject):
    """区切り線ブロック"""

    type: Literal[BlockType.DIVIDER] = Field(
        BlockType.DIVIDER, description="ブロックタイプ"
    )
    divider: EmptyObject = Field(
        default_factory=EmptyObject, description="空のコンテンツ"
    )


class BreadcrumbBlock(BaseBlockObject):
    """パンくずリストブロック"""

    type: Literal[BlockType.BREADCRUMB] = Field(
        BlockType.BREADCRUMB, description="ブロックタイプ"
    )
    breadcrumb: EmptyObject = Field(
        default_factory=EmptyObject, description="空のコンテンツ"
    )


class TableOfContentsBlock(BaseBlockObject):
    """目次ブロック"""

    type: Literal[BlockType.TABLE_OF_CONTENTS] = Field(
        BlockType.TABLE_OF_CONTENTS, description="ブロックタイプ"
    )
    table_of_contents: TableOfContentsContent = Field(..., description="目次コンテンツ")


class ColumnListBlock(BaseBlockObject):
    """カラムリストブロック"""

    type: Literal[BlockType.COLUMN_LIST] = Field(
        BlockType.COLUMN_LIST, description="ブロックタイプ"
    )
    column_list: EmptyObject = Field(
        default_factory=EmptyObject, description="空のコンテンツ"
    )


class ColumnBlock(BaseBlockObject):
    """カラムブロック"""

    type: Literal[BlockType.COLUMN] = Field(
        BlockType.COLUMN, description="ブロックタイプ"
    )
    column: ColumnContent = Field(..., description="カラムコンテンツ")


class LinkToPageBlock(BaseBlockObject):
    """ページへのリンクブロック"""

    type: Literal[BlockType.LINK_TO_PAGE] = Field(
        BlockType.LINK_TO_PAGE, description="ブロックタイプ"
    )
    link_to_page: LinkToPageContent = Field(..., description="リンクコンテンツ")


class TableBlock(BaseBlockObject):
    """テーブルブロック"""

    type: Literal[BlockType.TABLE] = Field(
        BlockType.TABLE, description="ブロックタイプ"
    )
    table: TableContent = Field(..., description="テーブルコンテンツ")


class TableRowBlock(BaseBlockObject):
    """テーブル行ブロック"""

    type: Literal[BlockType.TABLE_ROW] = Field(
        BlockType.TABLE_ROW, description="ブロックタイプ"
    )
    table_row: TableRowContent = Field(..., description="テーブル行コンテンツ")
