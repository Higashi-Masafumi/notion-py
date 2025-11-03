from typing import Literal
from pydantic import Field, StrictStr

from ._base_property import BaseProperty


class LastEditedTimeProperty(BaseProperty[Literal["last_edited_time"]]):
    """Notionのlast_edited_timeプロパティ"""

    type: Literal["last_edited_time"] = Field(
        "last_edited_time", description="プロパティタイプ"
    )

    last_edited_time: StrictStr = Field(..., description="最終編集日時（ISO 8601形式）")

    def get_display_value(self) -> str:
        """最終編集日時を取得

        Returns:
            StrictStr | None: 最終編集日時（未設定の場合はnull）
        """
        return self.last_edited_time
