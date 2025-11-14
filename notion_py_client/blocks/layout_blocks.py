"""
レイアウト系ブロックの定義

Divider, Breadcrumb, TableOfContents, ColumnList, Column, LinkToPage, Table, TableRow
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr

from .base import ApiColor, BaseBlockObject
from ..models.rich_text_item import RichTextItem, rich_text_to_markdown


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

    type: Literal["divider"] = Field("divider", description="ブロックタイプ")
    divider: EmptyObject = Field(
        default_factory=EmptyObject, description="空のコンテンツ"
    )

    def to_markdown(self) -> str:
        """区切り線ブロックをMarkdown形式に変換"""
        return "---"


class BreadcrumbBlock(BaseBlockObject):
    """パンくずリストブロック"""

    type: Literal["breadcrumb"] = Field("breadcrumb", description="ブロックタイプ")
    breadcrumb: EmptyObject = Field(
        default_factory=EmptyObject, description="空のコンテンツ"
    )

    def to_markdown(self) -> str:
        """パンくずリストブロックをMarkdown形式に変換"""
        return ""


class TableOfContentsBlock(BaseBlockObject):
    """目次ブロック"""

    type: Literal["table_of_contents"] = Field(
        "table_of_contents", description="ブロックタイプ"
    )
    table_of_contents: TableOfContentsContent = Field(..., description="目次コンテンツ")

    def to_markdown(self) -> str:
        """目次ブロックをMarkdown形式に変換"""
        return "[TOC]"


class ColumnListBlock(BaseBlockObject):
    """カラムリストブロック"""

    type: Literal["column_list"] = Field("column_list", description="ブロックタイプ")
    column_list: EmptyObject = Field(
        default_factory=EmptyObject, description="空のコンテンツ"
    )

    def to_markdown(self) -> str:
        """カラムリストブロックをMarkdown形式に変換"""
        return ""


class ColumnBlock(BaseBlockObject):
    """カラムブロック"""

    type: Literal["column"] = Field("column", description="ブロックタイプ")
    column: ColumnContent = Field(..., description="カラムコンテンツ")

    def to_markdown(self) -> str:
        """カラムブロックをMarkdown形式に変換"""
        return ""


class LinkToPageBlock(BaseBlockObject):
    """ページへのリンクブロック"""

    type: Literal["link_to_page"] = Field("link_to_page", description="ブロックタイプ")
    link_to_page: LinkToPageContent = Field(..., description="リンクコンテンツ")

    def to_markdown(self) -> str:
        """ページへのリンクブロックをMarkdown形式に変換"""
        if self.link_to_page.page_id:
            return f"[Page Link](https://notion.so/{self.link_to_page.page_id.replace('-', '')})"
        elif self.link_to_page.database_id:
            return f"[Database Link](https://notion.so/{self.link_to_page.database_id.replace('-', '')})"
        elif self.link_to_page.comment_id:
            return f"[Comment Link](https://notion.so/comment/{self.link_to_page.comment_id.replace('-', '')})"
        return ""


class TableBlock(BaseBlockObject):
    """テーブルブロック"""

    type: Literal["table"] = Field("table", description="ブロックタイプ")
    table: TableContent = Field(..., description="テーブルコンテンツ")

    def to_markdown(self) -> str:
        """テーブルブロックをMarkdown形式に変換"""
        return ""


class TableRowBlock(BaseBlockObject):
    """テーブル行ブロック"""

    type: Literal["table_row"] = Field("table_row", description="ブロックタイプ")
    table_row: TableRowContent = Field(..., description="テーブル行コンテンツ")

    def to_markdown(self) -> str:
        """テーブル行ブロックをMarkdown形式に変換"""
        cells = [rich_text_to_markdown(cell) for cell in self.table_row.cells]
        return "| " + " | ".join(cells) + " |"
