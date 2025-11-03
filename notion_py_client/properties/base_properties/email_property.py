from typing import Literal

from pydantic import Field, StrictStr

from ._base_property import BaseProperty


class EmailProperty(BaseProperty[Literal["email"]]):
    """Notionのemailプロパティ"""

    type: Literal["email"] = Field("email", description="プロパティタイプ")

    email: StrictStr | None = Field(
        None, description="メールアドレス（未設定の場合はnull）"
    )

    def get_display_value(self) -> str | None:
        """メールアドレスを取得

        Returns:
            StrictStr | None: メールアドレス（未設定の場合はnull）
        """
        return self.email
