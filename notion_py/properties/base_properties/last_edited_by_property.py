from typing import Literal

from pydantic import Field

from ...models import PartialUser, User
from ._base_property import BaseProperty, NotionPropertyType


class LastEditedByProperty(BaseProperty):
    """Notionのlast_edited_byプロパティ"""

    type: Literal[NotionPropertyType.LAST_EDITED_BY] = Field(
        NotionPropertyType.LAST_EDITED_BY, description="プロパティタイプ"
    )

    last_edited_by: PartialUser | User = Field(..., description="最終編集者情報")

    def get_value(self) -> str:
        """last_edited_by プロパティから最終編集者名を取得"""
        name = getattr(self.last_edited_by, "name", None)
        return name or ""
