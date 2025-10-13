from typing import Literal

from pydantic import Field, StrictStr

from ._base_property import BaseProperty, NotionPropertyType


class EmailProperty(BaseProperty[Literal[NotionPropertyType.EMAIL]]):
    """Notionのemailプロパティ"""

    type: Literal[NotionPropertyType.EMAIL] = Field(
        NotionPropertyType.EMAIL, description="プロパティタイプ"
    )

    email: StrictStr | None = Field(
        None, description="メールアドレス（未設定の場合はnull）"
    )

    def get_display_value(self) -> StrictStr | int | float | bool | None:
        """メールアドレスを取得

        Returns:
            StrictStr | None: メールアドレス（未設定の場合はnull）
        """
        return self.email
