from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, StrictStr

from .primitives import Annotations, Equation, Mention, Text


class RichTextItem(BaseModel):
    """NotionのRichText要素"""

    type: Literal["text", "mention", "equation"] = Field(
        ..., description="RichTextタイプ"
    )
    text: Text | None = Field(None, description="textタイプの内容")
    mention: Mention | None = Field(None, description="mentionタイプの内容")
    equation: Equation | None = Field(None, description="equationタイプの内容")
    annotations: Annotations = Field(..., description="アノテーション情報")
    plain_text: StrictStr = Field(..., description="プレーンテキスト")
    href: StrictStr | None = Field(None, description="リンクURL")

    def get_plain_text(self) -> str:
        """RichTextItemのプレーンテキストを取得"""
        return self.plain_text

    def to_markdown(self) -> str:
        """RichTextItemをMarkdown形式に変換"""
        text = self.plain_text

        # Apply code annotation exclusively (code blocks can't have other formatting)
        if self.annotations.code:
            # For code, we only need to escape backticks
            escaped_text = text.replace("`", "\\`")
            text = f"`{escaped_text}`"
            if self.href:
                text = f"[{text}]({self.href})"
            return text

        # Apply bold and italic (combined for better markdown)
        if self.annotations.bold and self.annotations.italic:
            text = f"***{text}***"
        elif self.annotations.bold:
            text = f"**{text}**"
        elif self.annotations.italic:
            text = f"*{text}*"

        # Apply strikethrough
        if self.annotations.strikethrough:
            text = f"~~{text}~~"

        # Apply link
        if self.href:
            text = f"[{text}]({self.href})"

        return text


def rich_text_to_markdown(rich_text: list[RichTextItem]) -> str:
    """RichTextItemのリストをMarkdown文字列に変換"""
    return "".join([item.to_markdown() for item in rich_text])
