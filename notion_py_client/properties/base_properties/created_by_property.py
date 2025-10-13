from typing import Literal

from pydantic import Field

from ...models import PartialUser, User
from ._base_property import BaseProperty, NotionPropertyType


class CreatedByProperty(BaseProperty[Literal[NotionPropertyType.CREATED_BY]]):
    """Notionのcreated_byプロパティ"""

    type: Literal[NotionPropertyType.CREATED_BY] = Field(
        NotionPropertyType.CREATED_BY, description="プロパティタイプ"
    )

    created_by: PartialUser | User = Field(..., description="作成者情報")

    def get_display_value(self) -> str | int | float | bool | None:
        """作成者情報を取得

        Returns:
            str | None: 作成者名。作成者情報が不完全な場合はNone
        """
        name = getattr(self.created_by, "name", None)
        return name if name else None
