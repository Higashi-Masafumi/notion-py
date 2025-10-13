from typing import Literal

from pydantic import Field, StrictStr

from ._base_property import BaseProperty, NotionPropertyType


class LastVisitedTimeProperty(
    BaseProperty[Literal[NotionPropertyType.LAST_VISITED_TIME]]
):
    """Notionのlast_visited_timeプロパティ"""

    type: Literal[NotionPropertyType.LAST_VISITED_TIME] = Field(
        NotionPropertyType.LAST_VISITED_TIME, description="プロパティタイプ"
    )

    last_visited_time: StrictStr | None = Field(
        None, description="最終表示日時（ISO 8601形式）"
    )

    def get_display_value(self) -> StrictStr | int | float | bool | None:
        """最終表示日時を取得

        Returns:
            StrictStr | None: 最終表示日時（未設定の場合はnull）
        """
        return self.last_visited_time
