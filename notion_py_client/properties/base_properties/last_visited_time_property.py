from typing import Literal

from pydantic import Field, StrictStr

from ._base_property import BaseProperty


class LastVisitedTimeProperty(BaseProperty[Literal["last_visited_time"]]):
    """Notionのlast_visited_timeプロパティ"""

    type: Literal["last_visited_time"] = Field(
        "last_visited_time", description="プロパティタイプ"
    )

    last_visited_time: StrictStr | None = Field(
        None, description="最終表示日時（ISO 8601形式）"
    )

    def get_display_value(self) -> str | None:
        """最終表示日時を取得

        Returns:
            StrictStr | None: 最終表示日時（未設定の場合はnull）
        """
        return self.last_visited_time
