from typing import Literal

from pydantic import Field, StrictStr

from ._base_property import BaseProperty, NotionPropertyType


class EmailProperty(BaseProperty):
    """Notionのemailプロパティ"""

    type: Literal[NotionPropertyType.EMAIL] = Field(
        NotionPropertyType.EMAIL, description="プロパティタイプ"
    )

    email: StrictStr | None = Field(
        None, description="メールアドレス（未設定の場合はnull）"
    )

    def get_value(self) -> str | None:
        """email プロパティからメールアドレスを取得"""
        return self.email
