from typing import Literal
from pydantic import Field, StrictStr

from ._base_property import BaseProperty


class UrlProperty(BaseProperty[Literal["url"]]):
    """Notionのurlプロパティ"""

    type: Literal["url"] = Field("url", description="プロパティタイプ")

    url: StrictStr | None = Field(None, description="URL（設定されていない場合はnull）")

    def get_display_value(self) -> str | None:
        """URLを取得

        Returns:
            StrictStr | None: URL（未設定の場合はnull）
        """
        return self.url
