from typing import Literal
from pydantic import Field

from ...models import StatusOption
from ._base_property import BaseProperty, NotionPropertyType


class StatusProperty(BaseProperty):
    """Notionのstatusプロパティ"""

    type: Literal[NotionPropertyType.STATUS] = Field(
        NotionPropertyType.STATUS, description="プロパティタイプ"
    )

    status: StatusOption | None = Field(
        None, description="現在のステータス（設定されていない場合はnull）"
    )

    def get_value(self) -> str | None:
        """
        status プロパティから現在のステータス名を取得

        Returns:
            str | None: ステータス名、未設定の場合はNone

        Note:
            - statusプロパティはselectと似ていますが、進捗管理に特化したプロパティです

        Examples:
            - 進行中: "進行中"
            - 完了: "完了"
            - 未設定: None
        """
        return self.status.name if self.status else None
