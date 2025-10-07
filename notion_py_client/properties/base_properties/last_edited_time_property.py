from typing import Literal
from pydantic import Field, StrictStr

from ._base_property import BaseProperty, NotionPropertyType


class LastEditedTimeProperty(BaseProperty):
    """Notionのlast_edited_timeプロパティ"""

    type: Literal[NotionPropertyType.LAST_EDITED_TIME] = Field(
        NotionPropertyType.LAST_EDITED_TIME, description="プロパティタイプ"
    )

    last_edited_time: StrictStr = Field(..., description="最終編集日時（ISO 8601形式）")

    def get_value(self) -> str:
        """
        last_edited_time プロパティから最終編集日時を取得

        Returns:
            str: 最終編集日時（ISO 8601形式）

        Examples:
            - "2025-09-23T02:14:00.000Z"
        """
        return self.last_edited_time
