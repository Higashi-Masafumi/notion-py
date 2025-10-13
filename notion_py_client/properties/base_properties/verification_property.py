from typing import Literal

from pydantic import Field

from ...models import Verification
from ._base_property import BaseProperty, NotionPropertyType


class VerificationProperty(BaseProperty[Literal[NotionPropertyType.VERIFICATION]]):
    """Notionのverificationプロパティ"""

    type: Literal[NotionPropertyType.VERIFICATION] = Field(
        NotionPropertyType.VERIFICATION, description="プロパティタイプ"
    )

    verification: Verification | None = Field(None, description="検証状態情報")

    def get_display_value(self) -> str | None:
        """検証状態情報を取得

        Returns:
            str | None: 検証状態情報の文字列表現。未設定の場合はNone
        """
        if self.verification is None:
            return None
        return self.verification.state
