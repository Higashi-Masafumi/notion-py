from typing import Literal

from pydantic import Field

from ...models import PartialUser, User
from ._base_property import BaseProperty


class LastEditedByProperty(BaseProperty[Literal["last_edited_by"]]):
    """Notionのlast_edited_byプロパティ"""

    type: Literal["last_edited_by"] = Field(
        "last_edited_by", description="プロパティタイプ"
    )

    last_edited_by: PartialUser | User = Field(..., description="最終編集者情報")

    def get_display_value(self) -> str | None:
        """最終編集者情報を取得

        Returns:
            str | None: 最終編集者名。最終編集者情報が不完全な場合はNone
        """
        name = getattr(self.last_edited_by, "name", None)
        return name if name else None
