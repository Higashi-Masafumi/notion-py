from typing import Literal

from pydantic import Field, StrictStr

from ._base_property import BaseProperty


class CreatedTimeProperty(BaseProperty[Literal["created_time"]]):
    """Notionのcreated_timeプロパティ"""

    type: Literal["created_time"] = Field(
        "created_time", description="プロパティタイプ"
    )

    created_time: StrictStr = Field(..., description="作成日時（ISO 8601形式）")

    def get_display_value(self) -> str:
        """作成日時を取得

        Returns:
            StrictStr | None: 作成日時（未設定の場合はnull）
        """
        return self.created_time
