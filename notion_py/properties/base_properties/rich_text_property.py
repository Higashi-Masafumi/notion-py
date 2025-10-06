from typing import Literal
from pydantic import Field

from ...models import RichTextItem
from ._base_property import BaseProperty, NotionPropertyType


class RichTextProperty(BaseProperty):
    """
    Notionのrich_textプロパティ

    複数のRichTextItemで構成される、書式付きテキストを表現するプロパティ
    """

    type: Literal[NotionPropertyType.RICH_TEXT] = Field(
        NotionPropertyType.RICH_TEXT, description="プロパティタイプ"
    )

    rich_text: list[RichTextItem] = Field(..., description="RichText要素の配列")

    def get_value(self) -> str:
        """
        rich_text プロパティからプレーンテキストを取得

        Returns:
            str: リッチテキストの内容をプレーンテキストとして結合した文字列

        Note:
            - 複数のRichTextItemのplain_textを結合します
            - 書式情報（太字、色等）は失われます
            - 空の場合は空文字列を返します

        Examples:
            - 通常テキスト: "これは説明文です"
            - 書式付き: "重要な情報です"（書式は除去）
            - 複数要素: "第一段落第二段落"（結合される）
            - 空: ""
        """
        return "".join(item.plain_text for item in self.rich_text)
