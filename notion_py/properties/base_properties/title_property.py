from typing import Literal
from pydantic import Field

from ...models import RichTextItem
from ._base_property import BaseProperty, NotionPropertyType


class TitleProperty(BaseProperty):
    """Notionのtitleプロパティ"""

    type: Literal[NotionPropertyType.TITLE] = Field(
        NotionPropertyType.TITLE, description="プロパティタイプ"
    )

    title: list[RichTextItem] = Field(..., description="タイトルのRichText配列")

    def get_value(self) -> str:
        """
        title プロパティからタイトルのプレーンテキストを取得

        Returns:
            str: タイトルの内容をプレーンテキストとして結合した文字列

        Note:
            - titleプロパティはrich_textと同様の構造ですが、ページのメインタイトルを表します
            - 書式情報（太字、色等）は失われます

        Examples:
            - 通常タイトル: "プロジェクトA"
            - 空のタイトル: ""
        """
        return "".join(item.plain_text for item in self.title)
