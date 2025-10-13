from typing import Literal

from pydantic import Field

from ...models import PartialUser, User
from ._base_property import BaseProperty, NotionPropertyType


class LastEditedByProperty(BaseProperty[Literal[NotionPropertyType.LAST_EDITED_BY]]):
    """Notionのlast_edited_byプロパティ"""

    type: Literal[NotionPropertyType.LAST_EDITED_BY] = Field(
        NotionPropertyType.LAST_EDITED_BY, description="プロパティタイプ"
    )

    last_edited_by: PartialUser | User = Field(..., description="最終編集者情報")

    def get_display_value(self) -> str | None:
        """最終編集者情報を取得

        Returns:
            str | None: 最終編集者名。最終編集者情報が不完全な場合はNone
        """
        name = getattr(self.last_edited_by, "name", None)
        return name if name else None
