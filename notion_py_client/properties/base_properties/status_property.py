from typing import Literal
from pydantic import Field

from ...models import StatusOption
from ._base_property import BaseProperty, NotionPropertyType


class StatusProperty(BaseProperty[Literal[NotionPropertyType.STATUS]]):
    """Notionのstatusプロパティ"""

    type: Literal[NotionPropertyType.STATUS] = Field(
        NotionPropertyType.STATUS, description="プロパティタイプ"
    )

    status: StatusOption | None = Field(
        None, description="現在のステータス（設定されていない場合はnull）"
    )

    def get_display_value(self) -> str | None:
        """選択されたステータス名を取得

        Returns:
            str | None: 選択されたステータス名。未設定の場合はNone
        """
        if self.status is None:
            return None
        return self.status.name
