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
