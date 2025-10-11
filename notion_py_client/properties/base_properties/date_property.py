from pydantic import Field

from ...models import DateInfo
from ._base_property import BaseProperty, NotionPropertyType
from typing import Literal
from datetime import date as dt_date


class DateProperty(BaseProperty[Literal[NotionPropertyType.DATE]]):
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

    def get_start_date(self) -> dt_date:
        """
        date プロパティから開始日を date 型で取得

        Returns:
            date: 開始日（date型）
        Raises:
            ValueError: dateプロパティが未設定の場合
        Note:
            - 日付範囲が設定されている場合も開始日のみを返します
            - 終了日が必要な場合は、date.endを直接参照してください

        Examples:
            - 単一日付: date(2024, 3, 15)
            - 日付範囲: date(2024, 3, 15) (開始日のみ)
            - 未設定: None
        """
        if not self.date:
            raise ValueError("Date property is not set")
        return dt_date.fromisoformat(self.date.start)

    def get_end_date(self) -> dt_date:
        """
        date プロパティから終了日を date 型で取得

        Returns:
            date: 終了日（date型）
        Raises:
            ValueError: 終了日が設定されていない場合
        Note:
            - 単一日付の場合、終了日はNoneとなります
            - 終了日が必要な場合は、date.endを直接参照してください

        Examples:
            - 単一日付: None
            - 日付範囲: date(2024, 3, 20) (終了日のみ)
            - 未設定: None
        """
        if not self.date or not self.date.end:
            raise ValueError("End date is not set")
        return dt_date.fromisoformat(self.date.end)
