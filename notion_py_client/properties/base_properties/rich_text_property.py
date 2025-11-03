from typing import Literal
from pydantic import Field

from ...models import RichTextItem
from ._base_property import BaseProperty


class RichTextProperty(BaseProperty[Literal["rich_text"]]):
    """
    Notionのrich_textプロパティ

    複数のRichTextItemで構成される、書式付きテキストを表現するプロパティ
    """

    type: Literal["rich_text"] = Field("rich_text", description="プロパティタイプ")

    rich_text: list[RichTextItem] = Field(..., description="RichText要素の配列")

    def get_display_value(self) -> str | None:
        """リッチテキストの内容を取得

        Returns:
            str | None: リッチテキストの内容を連結した文字列。リッチテキストが空の場合はNone
        """
        if len(self.rich_text) == 0:
            return None
        return "".join(item.plain_text for item in self.rich_text)
