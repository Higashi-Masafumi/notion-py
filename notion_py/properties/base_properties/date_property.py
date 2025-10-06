from pydantic import Field

from ...models import DateInfo
from ._base_property import BaseProperty, NotionPropertyType
from typing import Literal


class DateProperty(BaseProperty):
    """Notionのdateプロパティ"""

    type: Literal[NotionPropertyType.DATE] = Field(
        NotionPropertyType.DATE, description="プロパティタイプ"
    )
    date: DateInfo | None = Field(
        None, description="日付情報（設定されていない場合はnull）"
    )

    def get_value(self) -> str | None:
        """
        date プロパティから開始日を取得

        Returns:
            str | None: 開始日（ISO8601形式文字列）、未設定の場合はNone

        Note:
            - 日付範囲が設定されている場合も開始日のみを返します
            - 終了日が必要な場合は、date.endを直接参照してください

        Examples:
            - 単一日付: "2024-03-15"
            - 日付範囲: "2024-03-15" (開始日のみ)
            - 未設定: None
        """
        return self.date.start if self.date else None
