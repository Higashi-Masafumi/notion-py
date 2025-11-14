"""
テキスト系ブロックの定義

Paragraph, Heading1/2/3, BulletedListItem, NumberedListItem, Quote, ToDo, Toggle, Template
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, StrictBool

from .base import ApiColor, BaseBlockObject
from ..models.rich_text_item import RichTextItem, rich_text_to_markdown


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

    def to_markdown(self) -> str:
        """段落ブロックをMarkdown形式に変換"""
        return rich_text_to_markdown(self.paragraph.rich_text)


class Heading1Block(BaseBlockObject):
    """見出し1ブロック"""

    type: Literal["heading_1"] = Field("heading_1", description="ブロックタイプ")
    heading_1: HeaderContentWithRichTextAndColor = Field(
        ..., description="見出し1コンテンツ"
    )

    def to_markdown(self) -> str:
        """見出し1ブロックをMarkdown形式に変換"""

        return f"# {rich_text_to_markdown(self.heading_1.rich_text)}"


class Heading2Block(BaseBlockObject):
    """見出し2ブロック"""

    type: Literal["heading_2"] = Field("heading_2", description="ブロックタイプ")
    heading_2: HeaderContentWithRichTextAndColor = Field(
        ..., description="見出し2コンテンツ"
    )

    def to_markdown(self) -> str:
        """見出し2ブロックをMarkdown形式に変換"""

        return f"## {rich_text_to_markdown(self.heading_2.rich_text)}"


class Heading3Block(BaseBlockObject):
    """見出し3ブロック"""

    type: Literal["heading_3"] = Field("heading_3", description="ブロックタイプ")
    heading_3: HeaderContentWithRichTextAndColor = Field(
        ..., description="見出し3コンテンツ"
    )

    def to_markdown(self) -> str:
        """見出し3ブロックをMarkdown形式に変換"""

        return f"### {rich_text_to_markdown(self.heading_3.rich_text)}"


class BulletedListItemBlock(BaseBlockObject):
    """箇条書きリストアイテムブロック"""

    type: Literal["bulleted_list_item"] = Field(
        "bulleted_list_item", description="ブロックタイプ"
    )
    bulleted_list_item: ContentWithRichTextAndColor = Field(
        ..., description="箇条書きリストアイテムコンテンツ"
    )

    def to_markdown(self) -> str:
        """箇条書きリストアイテムブロックをMarkdown形式に変換"""

        return f"- {rich_text_to_markdown(self.bulleted_list_item.rich_text)}"


class NumberedListItemBlock(BaseBlockObject):
    """番号付きリストアイテムブロック"""

    type: Literal["numbered_list_item"] = Field(
        "numbered_list_item", description="ブロックタイプ"
    )
    numbered_list_item: ContentWithRichTextAndColor = Field(
        ..., description="番号付きリストアイテムコンテンツ"
    )

    def to_markdown(self) -> str:
        """番号付きリストアイテムブロックをMarkdown形式に変換"""

        return f"1. {rich_text_to_markdown(self.numbered_list_item.rich_text)}"


class QuoteBlock(BaseBlockObject):
    """引用ブロック"""

    type: Literal["quote"] = Field("quote", description="ブロックタイプ")
    quote: ContentWithRichTextAndColor = Field(..., description="引用コンテンツ")

    def to_markdown(self) -> str:
        """引用ブロックをMarkdown形式に変換"""

        return f"> {rich_text_to_markdown(self.quote.rich_text)}"


class ToDoContent(BaseModel):
    """ToDoコンテンツ"""

    rich_text: list[RichTextItem] = Field(..., description="リッチテキスト配列")
    color: ApiColor = Field(..., description="カラー設定")
    checked: StrictBool | None = Field(None, description="チェック状態")


class ToDoBlock(BaseBlockObject):
    """ToDoブロック"""

    type: Literal["to_do"] = Field("to_do", description="ブロックタイプ")
    to_do: ToDoContent = Field(..., description="ToDoコンテンツ")

    def to_markdown(self) -> str:
        """ToDoブロックをMarkdown形式に変換"""

        checkbox = "[x]" if self.to_do.checked else "[ ]"
        return f"- {checkbox} {rich_text_to_markdown(self.to_do.rich_text)}"


class ToggleBlock(BaseBlockObject):
    """トグルブロック"""

    type: Literal["toggle"] = Field("toggle", description="ブロックタイプ")
    toggle: ContentWithRichTextAndColor = Field(..., description="トグルコンテンツ")

    def to_markdown(self) -> str:
        """トグルブロックをMarkdown形式に変換"""

        return f"<details><summary>{rich_text_to_markdown(self.toggle.rich_text)}</summary></details>"


class TemplateBlock(BaseBlockObject):
    """テンプレートブロック"""

    type: Literal["template"] = Field("template", description="ブロックタイプ")
    template: ContentWithRichTextAndColor = Field(
        ..., description="テンプレートコンテンツ"
    )

    def to_markdown(self) -> str:
        """テンプレートブロックをMarkdown形式に変換"""

        return rich_text_to_markdown(self.template.rich_text)
