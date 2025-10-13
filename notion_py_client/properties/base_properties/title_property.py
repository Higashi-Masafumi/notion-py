from typing import Literal
from pydantic import Field

from ...models import RichTextItem
from ._base_property import BaseProperty, NotionPropertyType


class TitleProperty(BaseProperty[Literal[NotionPropertyType.TITLE]]):
    """Notionのtitleプロパティ"""

    type: Literal[NotionPropertyType.TITLE] = Field(
        NotionPropertyType.TITLE, description="プロパティタイプ"
    )

    title: list[RichTextItem] = Field(..., description="タイトルのRichText配列")

    def get_display_value(self) -> str | int | float | bool | None:
        """タイトルの内容を取得

        Returns:
            str | None: タイトルの内容を連結した文字列。タイトルが空の場合はNone
        """
        if len(self.title) == 0:
            return None
        return "".join(item.plain_text for item in self.title)
