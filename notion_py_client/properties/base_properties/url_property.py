from typing import Literal
from pydantic import Field, StrictStr

from ._base_property import BaseProperty, NotionPropertyType


class UrlProperty(BaseProperty[Literal[NotionPropertyType.URL]]):
    """Notionのurlプロパティ"""

    type: Literal[NotionPropertyType.URL] = Field(
        NotionPropertyType.URL, description="プロパティタイプ"
    )

    url: StrictStr | None = Field(None, description="URL（設定されていない場合はnull）")

    def get_display_value(self) -> StrictStr | int | float | bool | None:
        """URLを取得

        Returns:
            StrictStr | None: URL（未設定の場合はnull）
        """
        return self.url
