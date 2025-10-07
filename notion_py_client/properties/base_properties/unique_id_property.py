from typing import Literal

from pydantic import Field

from ...models import UniqueId
from ._base_property import BaseProperty, NotionPropertyType


class UniqueIdProperty(BaseProperty):
    """Notionのunique_idプロパティ"""

    type: Literal[NotionPropertyType.UNIQUE_ID] = Field(
        NotionPropertyType.UNIQUE_ID, description="プロパティタイプ"
    )

    unique_id: UniqueId = Field(..., description="ユニークIDの値")

    def get_value(self) -> UniqueId:
        """unique_id プロパティの値を返す"""
        return self.unique_id
