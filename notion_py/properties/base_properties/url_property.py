from typing import Literal
from pydantic import Field, StrictStr

from ._base_property import BaseProperty, NotionPropertyType


class UrlProperty(BaseProperty):
    """Notionのurlプロパティ"""

    type: Literal[NotionPropertyType.URL] = Field(
        NotionPropertyType.URL, description="プロパティタイプ"
    )

    url: StrictStr | None = Field(None, description="URL（設定されていない場合はnull）")

    def get_value(self) -> str | None:
        """
        url プロパティからURLを取得

        Returns:
            str | None: URL文字列、未設定の場合はNone

        Examples:
            - 有効なURL: "https://example.com"
            - 未設定: None
        """
        return self.url
