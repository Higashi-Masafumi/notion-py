from typing import Literal

from pydantic import Field

from ...models import PartialUser, User
from ._base_property import BaseProperty


class CreatedByProperty(BaseProperty[Literal["created_by"]]):
    """Notionのcreated_byプロパティ"""

    type: Literal["created_by"] = Field("created_by", description="プロパティタイプ")

    created_by: PartialUser | User = Field(..., description="作成者情報")

    def get_display_value(self) -> str | None:
        """作成者情報を取得

        Returns:
            str | None: 作成者名。作成者情報が不完全な場合はNone
        """
        name = getattr(self.created_by, "name", None)
        return name if name else None
