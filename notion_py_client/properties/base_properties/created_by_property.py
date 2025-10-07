from typing import Literal

from pydantic import Field

from ...models import PartialUser, User
from ._base_property import BaseProperty, NotionPropertyType


class CreatedByProperty(BaseProperty):
    """Notionのcreated_byプロパティ"""

    type: Literal[NotionPropertyType.CREATED_BY] = Field(
        NotionPropertyType.CREATED_BY, description="プロパティタイプ"
    )

    created_by: PartialUser | User = Field(..., description="作成者情報")

    def get_value(self) -> str:
        """created_by プロパティから作成者名を取得"""
        name = getattr(self.created_by, "name", None)
        return name or ""
