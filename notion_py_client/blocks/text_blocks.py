"""
テキスト系ブロックの定義

Paragraph, Heading1/2/3, BulletedListItem, NumberedListItem, Quote, ToDo, Toggle, Template
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, StrictBool

from .base import ApiColor, BaseBlockObject
from ..models.rich_text_item import RichTextItem


class ContentWithRichTextAndColor(BaseModel):
    """リッチテキストとカラーを持つコンテンツ"""

    rich_text: list[RichTextItem] = Field(..., description="リッチテキスト配列")
    color: ApiColor = Field(..., description="カラー設定")


class HeaderContentWithRichTextAndColor(BaseModel):
    """ヘッダー用リッチテキストとカラーを持つコンテンツ"""

    rich_text: list[RichTextItem] = Field(..., description="リッチテキスト配列")
    color: ApiColor = Field(..., description="カラー設定")
    is_toggleable: StrictBool = Field(..., description="トグル可能かどうか")


# ============================================
# Text Blocks
# ============================================


class ParagraphBlock(BaseBlockObject):
    """段落ブロック"""

    type: Literal["paragraph"] = Field("paragraph", description="ブロックタイプ")
    paragraph: ContentWithRichTextAndColor = Field(..., description="段落コンテンツ")


class Heading1Block(BaseBlockObject):
    """見出し1ブロック"""

    type: Literal["heading_1"] = Field("heading_1", description="ブロックタイプ")
    heading_1: HeaderContentWithRichTextAndColor = Field(
        ..., description="見出し1コンテンツ"
    )


class Heading2Block(BaseBlockObject):
    """見出し2ブロック"""

    type: Literal["heading_2"] = Field("heading_2", description="ブロックタイプ")
    heading_2: HeaderContentWithRichTextAndColor = Field(
        ..., description="見出し2コンテンツ"
    )


class Heading3Block(BaseBlockObject):
    """見出し3ブロック"""

    type: Literal["heading_3"] = Field("heading_3", description="ブロックタイプ")
    heading_3: HeaderContentWithRichTextAndColor = Field(
        ..., description="見出し3コンテンツ"
    )


class BulletedListItemBlock(BaseBlockObject):
    """箇条書きリストアイテムブロック"""

    type: Literal["bulleted_list_item"] = Field(
        "bulleted_list_item", description="ブロックタイプ"
    )
    bulleted_list_item: ContentWithRichTextAndColor = Field(
        ..., description="箇条書きリストアイテムコンテンツ"
    )


class NumberedListItemBlock(BaseBlockObject):
    """番号付きリストアイテムブロック"""

    type: Literal["numbered_list_item"] = Field(
        "numbered_list_item", description="ブロックタイプ"
    )
    numbered_list_item: ContentWithRichTextAndColor = Field(
        ..., description="番号付きリストアイテムコンテンツ"
    )


class QuoteBlock(BaseBlockObject):
    """引用ブロック"""

    type: Literal["quote"] = Field("quote", description="ブロックタイプ")
    quote: ContentWithRichTextAndColor = Field(..., description="引用コンテンツ")


class ToDoContent(BaseModel):
    """ToDoコンテンツ"""

    rich_text: list[RichTextItem] = Field(..., description="リッチテキスト配列")
    color: ApiColor = Field(..., description="カラー設定")
    checked: StrictBool | None = Field(None, description="チェック状態")


class ToDoBlock(BaseBlockObject):
    """ToDoブロック"""

    type: Literal["to_do"] = Field("to_do", description="ブロックタイプ")
    to_do: ToDoContent = Field(..., description="ToDoコンテンツ")


class ToggleBlock(BaseBlockObject):
    """トグルブロック"""

    type: Literal["toggle"] = Field("toggle", description="ブロックタイプ")
    toggle: ContentWithRichTextAndColor = Field(..., description="トグルコンテンツ")


class TemplateBlock(BaseBlockObject):
    """テンプレートブロック"""

    type: Literal["template"] = Field("template", description="ブロックタイプ")
    template: ContentWithRichTextAndColor = Field(
        ..., description="テンプレートコンテンツ"
    )
