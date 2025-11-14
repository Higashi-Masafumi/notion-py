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

        # Apply annotations
        if self.annotations.bold:
            text = f"**{text}**"
        if self.annotations.italic:
            text = f"*{text}*"
        if self.annotations.strikethrough:
            text = f"~~{text}~~"
        if self.annotations.code:
            text = f"`{text}`"

        # Apply link
        if self.href:
            text = f"[{text}]({self.href})"

        return text


def rich_text_to_markdown(rich_text: list[RichTextItem]) -> str:
    """RichTextItemのリストをMarkdown文字列に変換"""
    return "".join([item.to_markdown() for item in rich_text])
