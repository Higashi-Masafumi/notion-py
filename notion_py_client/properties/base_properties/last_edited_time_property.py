from typing import Literal
from pydantic import Field, StrictStr

from ._base_property import BaseProperty, NotionPropertyType


class LastEditedTimeProperty(BaseProperty[Literal[NotionPropertyType.LAST_EDITED_TIME]]):
    """Notionのlast_edited_timeプロパティ"""

    type: Literal[NotionPropertyType.LAST_EDITED_TIME] = Field(
        NotionPropertyType.LAST_EDITED_TIME, description="プロパティタイプ"
    )

    last_edited_time: StrictStr = Field(..., description="最終編集日時（ISO 8601形式）")

    def get_display_value(self) -> str:
        """最終編集日時を取得

        Returns:
            StrictStr | None: 最終編集日時（未設定の場合はnull）
        """
        return self.last_edited_time
