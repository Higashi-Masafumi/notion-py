from typing import Literal

from pydantic import Field, StrictStr

from ._base_property import BaseProperty, NotionPropertyType


class CreatedTimeProperty(BaseProperty):
    """Notionのcreated_timeプロパティ"""

    type: Literal[NotionPropertyType.CREATED_TIME] = Field(
        NotionPropertyType.CREATED_TIME, description="プロパティタイプ"
    )

    created_time: StrictStr = Field(..., description="作成日時（ISO 8601形式）")

    def get_value(self) -> str:
        """created_time プロパティから作成日時を取得"""
        return self.created_time
