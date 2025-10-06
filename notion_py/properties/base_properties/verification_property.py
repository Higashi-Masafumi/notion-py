from typing import Literal

from pydantic import Field

from ...models import Verification
from ._base_property import BaseProperty, NotionPropertyType


class VerificationProperty(BaseProperty):
    """Notionのverificationプロパティ"""

    type: Literal[NotionPropertyType.VERIFICATION] = Field(
        NotionPropertyType.VERIFICATION, description="プロパティタイプ"
    )

    verification: Verification | None = Field(
        None, description="検証状態情報"
    )

    def get_value(self) -> Verification | None:
        """verification プロパティの値を返す"""
        return self.verification
